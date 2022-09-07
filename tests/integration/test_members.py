from unittest import TestCase
from family_tree.member import Gender, Member

class TestMember(TestCase):

    def setUp(self):
        self.member = Member(1, 'Vineet', 'Male')
        self.mother = Member(2, 'Mother', 'Female')
        self.father = Member(3, 'Father', 'Male')
        self.spouse = Member(4, 'Spouse', 'Female')

        self.son_a = Member(5, 'SonA', 'Male')
        self.son_b = Member(6, 'SonB', 'Male')
        self.daughter_a = Member(7, 'DaughterA', 'Female')
        self.daughter_b = Member(8, 'DaughterB', 'Female')

        self.sister_a = Member(9, 'SisterA', 'Female')
        self.sister_b = Member(10, 'SisterB', 'Female')
        self.brother_a = Member(11, 'BrotherA', 'Male')
        self.brother_b = Member(12, 'BrotherB', 'Male')

        self.paternal_grandmother = Member(13, 'PaternalGrandmother', 'Female')
        self.maternal_grandmother = Member(14, 'MaternalGrandmother', 'Female')

        self.father_sister_a = Member(15, 'PaternalAuntA', 'Female')
        self.father_sister_b = Member(16, 'PaternalAuntB', 'Female')
        self.father_brother_a = Member(17, 'PaternalUncleA', 'Male')
        self.father_brother_b = Member(18, 'PaternalUncleB', 'Male')

        self.mother_sister_a = Member(19, 'MaternalAuntA', 'Female')
        self.mother_sister_b = Member(20, 'MaternalAuntB', 'Female')
        self.mother_brother_a = Member(21, 'MaternalUncleA', 'Male')
        self.mother_brother_b = Member(22, 'MaternalUncleB', 'Male')

        self.member.set_mother(self.mother)
        self.member.set_father(self.father)
        self.member.set_spouse(self.spouse)
        self.member.spouse.set_spouse(self.member)

        self.member.add_child(self.son_a)
        self.member.add_child(self.son_b)
        self.member.add_child(self.daughter_a)
        self.member.add_child(self.daughter_b)

        self.father.add_child(self.sister_a)
        self.father.add_child(self.sister_b)
        self.father.add_child(self.brother_a)
        self.father.add_child(self.brother_b)
        self.father.add_child(self.member)

        self.mother.add_child(self.sister_a)
        self.mother.add_child(self.sister_b)
        self.mother.add_child(self.brother_a)
        self.mother.add_child(self.brother_b)
        self.mother.add_child(self.member)

        self.father.set_mother(self.paternal_grandmother)
        self.paternal_grandmother.add_child(self.father_sister_a)
        self.paternal_grandmother.add_child(self.father_sister_b)
        self.paternal_grandmother.add_child(self.father_brother_a)
        self.paternal_grandmother.add_child(self.father_brother_b)
        self.paternal_grandmother.add_child(self.father)

        self.mother.set_mother(self.maternal_grandmother)

        self.maternal_grandmother.add_child(self.mother_sister_a)
        self.maternal_grandmother.add_child(self.mother_sister_b)
        self.maternal_grandmother.add_child(self.mother_brother_a)
        self.maternal_grandmother.add_child(self.mother_brother_b)
        self.maternal_grandmother.add_child(self.mother)

    def test_set_methods(self):
        self.assertEqual(self.member.mother.name, "Mother")
        self.assertEqual(self.member.father.name, "Father")
        
        self.assertEqual(self.member in self.member.father.children, True)
        self.assertEqual(self.member in self.member.mother.children, True)

        self.assertEqual(len(self.member.mother.children), 5)
        self.assertEqual(self.brother_a in self.member.mother.children, True)
        self.assertEqual(self.brother_b in self.member.mother.children, True)
        self.assertEqual(self.sister_a in self.member.mother.children, True)
        self.assertEqual(self.sister_b in self.member.mother.children, True)

        self.assertEqual(len(self.member.father.children), 5)
        self.assertEqual(self.brother_a in self.member.father.children, True)
        self.assertEqual(self.brother_b in self.member.father.children, True)
        self.assertEqual(self.sister_a in self.member.father.children, True)
        self.assertEqual(self.sister_b in self.member.father.children, True)

        self.assertEqual(self.member.spouse.name, "Spouse")

        self.assertEqual(len(self.member.mother.mother.children), 5)
        self.assertEqual(self.member.mother in self.member.mother.mother.children, True)
        self.assertEqual(self.mother_brother_a in self.member.mother.mother.children, True)
        self.assertEqual(self.mother_brother_b in self.member.mother.mother.children, True)
        self.assertEqual(self.mother_sister_a in self.member.mother.mother.children, True)
        self.assertEqual(self.mother_sister_b in self.member.mother.mother.children, True)

        self.assertEqual(len(self.member.father.mother.children), 5)
        self.assertEqual(self.member.father in self.member.father.mother.children, True)
        self.assertEqual(self.father_brother_a in self.member.father.mother.children, True)
        self.assertEqual(self.father_brother_b in self.member.father.mother.children, True)
        self.assertEqual(self.father_sister_a in self.member.father.mother.children, True)
        self.assertEqual(self.father_sister_b in self.member.father.mother.children, True)

        self.assertEqual(len(self.member.children), 4)
        self.assertEqual(self.son_a in self.member.children, True)
        self.assertEqual(self.son_b in self.member.children, True)
        self.assertEqual(self.daughter_a in self.member.children, True)
        self.assertEqual(self.daughter_b in self.member.children, True)

    def test_get_methods(self):
        self.assertEqual(len(self.member.get_relationship("paternal_aunt")), 2)
        self.assertEqual(len(self.member.get_relationship("maternal_aunt")), 2)

        self.assertEqual(len(self.member.get_relationship("paternal_uncle")), 2)
        self.assertEqual(len(self.member.get_relationship("maternal_uncle")), 2)

        self.assertEqual(len(self.member.get_relationship("siblings")), 4)
        self.assertEqual(len(self.member.get_relationship("son")), 2)
        self.assertEqual(len(self.member.get_relationship("daughter")), 2)

        self.assertEqual(len(self.member.spouse.get_relationship("brother_in_law")), 2)
        self.assertEqual(len(self.member.spouse.get_relationship("sister_in_law")), 2)
