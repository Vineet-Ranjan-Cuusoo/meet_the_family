from unittest import TestCase
from unittest.mock import patch, Mock
from family_tree.member import Member, Gender

def create_fake_member(id=None, name=None, gender=None, mother=None, spouse=None, father=None, children=None):
    member=Mock()
    member.id = id
    member.name = name
    member.gender = gender
    member.mother = mother
    member.spouse = spouse
    member.father = father
    member.children = children
    return member

class TestMember(TestCase):

    def setUp(self):
        self.member = Member(1, "Zim", "Male")

    def test_initialization(self):
        # check instance
        self.assertEqual(isinstance(self.member, Member), True)

        # check properties
        self.assertEqual(self.member.id, 1)
        self.assertEqual(self.member.name, "Zim")
        self.assertEqual(self.member.gender, Gender.male)
        self.assertEqual(self.member.mother, None)
        self.assertEqual(self.member.father, None)
        self.assertEqual(self.member.spouse, None)
        self.assertEqual(self.member.children, [])

        # edge case for gender
        self.assertRaises(ValueError, Member, 2, "SomeOtherPerson", "Queer")

    def test_set_mother(self):
        mother_demo_a = "mother_demo_a"
        mother_demo_b = Member(2, "MotherDemoB", "Male")
        mother_demo_c = Member(3, "Mom", "Female")

        # error cases
        self.assertRaises(ValueError, self.member.set_mother, mother_demo_a)
        self.assertRaises(ValueError, self.member.set_mother, mother_demo_b)

        # success cases
        self.member.set_mother(mother_demo_c)
        self.assertEqual(self.member.mother.name, "Mom")
        self.assertEqual(self.member.mother.gender, Gender.female)

    def test_set_father(self):
        father_demo_a = "father_demo_a"
        father_demo_b = Member(4, "FatherDemoB", "Female")
        father_demo_c = Member(5, "Dad", "Male")

        # error cases
        self.assertRaises(ValueError, self.member.set_father, father_demo_a)
        self.assertRaises(ValueError, self.member.set_father, father_demo_b)

        # success cases
        self.member.set_father(father_demo_c)
        self.assertEqual(self.member.father.name, "Dad")
        self.assertEqual(self.member.father.gender, Gender.male)

    def test_set_spouse(self):
        spouse_demo_a = "spouse_demo_a"
        spouse_demo_b = Member(6, "SpouseDemoB", "Male")
        spouse_demo_c = Member(7, "Spouse", "Female")

        # error cases
        self.assertRaises(ValueError, self.member.set_spouse, spouse_demo_a)
        self.assertRaises(ValueError, self.member.set_spouse, spouse_demo_b)

        # success cases
        self.member.set_spouse(spouse_demo_c)
        self.assertEqual(self.member.spouse.name, "Spouse")
        self.assertEqual(self.member.spouse.gender, Gender.female)

    def test_add_child(self):
        child_demo_a = "child_demo_a"
        child_demo_b = Member(8, "Daughter", "Female")

        # error cases
        self.assertRaises(ValueError, self.member.add_child, child_demo_a)

        # success cases
        self.member.add_child(child_demo_b)
        self.assertEqual(len(self.member.children), 1)
        self.assertEqual(self.member.children[0].name, "Daughter")
        self.assertEqual(self.member.children[0].gender, Gender.female)
    
    def test_get_paternal_grandmother(self):
        member = Member(9, "NewMember", "Male")
        father = Member(10, "NewMember_father", "Male")
        grandmother = Member(11, "NewMember_grandmother", "Female")

        # error cases
        self.assertEqual(member.get_paternal_grandmother(), None)

        member.father = father
        self.assertEqual(member.get_paternal_grandmother(), None)

        member.father.mother = grandmother
        self.assertEqual(member.get_paternal_grandmother(), grandmother)

    def test_get_maternal_grandmother(self):
        member = Member(12, "NewMember", "Male")
        mother = Member(13, "NewMember_mother", "Female")
        grandmother = Member(14, "NewMember_grandmother", "Female")

        # error cases
        self.assertEqual(member.get_maternal_grandmother(), None)

        member.mother = mother
        self.assertEqual(member.get_maternal_grandmother(), None)

        member.mother.mother = grandmother
        self.assertEqual(member.get_maternal_grandmother(), grandmother)
    
    def test_get_spouse_mother(self):
        member = Member(15, "NewMember", "Male")
        spouse = Member(16, "NewMember_spouse", "Female")
        spouse_mother = Member(17, "NewMember_spouse_mother", "Female")

        # error cases
        self.assertEqual(member.get_spouse_mother(), None)

        member.spouse = spouse
        self.assertEqual(member.get_spouse_mother(), None)

        member.spouse.mother = spouse_mother
        self.assertEqual(member.get_spouse_mother(), spouse_mother)
    
    @patch('family_tree.member.Member.get_paternal_grandmother', side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[Member(5, "Dad", "Male")]),
        create_fake_member(children=[
          Member(5, "Dad", "Male"),
          Member(18, "Uncle", "Male")  
        ]),
        create_fake_member(children=[
          Member(5, "Dad", "Male"),
          Member(18, "Uncle", "Male"),
          Member(19, "Aunt", "Female")
        ])
    ])
    def test_get_paternal_aunt(self, mock_get_paternal_grandmother):
        
        # check if get_paternal_grandmother has been replaced by a Mock instance
        self.assertEqual(isinstance(self.member.get_paternal_grandmother, Mock), True)
    
        # check for None values
        self.assertEqual(self.member.get_paternal_aunt(), [])
        self.assertEqual(self.member.get_paternal_aunt(), [])
        self.assertEqual(self.member.get_paternal_aunt(), [])
        self.assertEqual(self.member.get_paternal_aunt(), [])

        paternal_aunts = self.member.get_paternal_aunt()
        self.assertEqual(len(paternal_aunts), 1)
        self.assertEqual(paternal_aunts[0].name, "Aunt")
        self.assertEqual(paternal_aunts[0].gender, Gender.female)

        # check that the mock_get_paternal_grandmother is called instead of self.member.get_paternal_grandmother
        mock_get_paternal_grandmother.assert_called_with()

    @patch('family_tree.member.Member.get_paternal_grandmother', side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[Member(5, "Dad", "Male")]),
        create_fake_member(children=[
          Member(5, "Dad", "Male"),
          Member(19, "Aunt", "Female")  
        ]),
        create_fake_member(children=[
          Member(5, "Dad", "Male"),
          Member(18, "Uncle", "Male"),
          Member(19, "Aunt", "Female")
        ])
    ])
    def test_get_paternal_uncle(self, mock_get_paternal_grandmother):
        
        self.member.father = Member(5, "Dad", "Male")

        # check if get_paternal_grandmother has been replaced by a Mock instance
        self.assertEqual(isinstance(self.member.get_paternal_grandmother, Mock), True)
    
        # check for None values
        self.assertEqual(self.member.get_paternal_uncle(), [])
        self.assertEqual(self.member.get_paternal_uncle(), [])
        self.assertEqual(self.member.get_paternal_uncle(), [])
        self.assertEqual(self.member.get_paternal_uncle(), [])

        paternal_uncles = self.member.get_paternal_uncle()
        self.assertEqual(len(paternal_uncles), 1)
        self.assertEqual(paternal_uncles[0].name, "Uncle")
        self.assertEqual(paternal_uncles[0].gender, Gender.male)

        # check that the mock_get_paternal_grandmother is called instead of self.member.get_paternal_grandmother
        mock_get_paternal_grandmother.assert_called_with()  

    @patch('family_tree.member.Member.get_maternal_grandmother', side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[Member(3, "Mom", "Female")]),
        create_fake_member(children=[
          Member(3, "Mom", "Female"),
          Member(19, "Uncle", "Male")  
        ]),
        create_fake_member(children=[
          Member(3, "Mom", "Female"),
          Member(19, "Uncle", "Male"),
          Member(20, "Aunt", "Female")
        ])
    ])
    def test_get_maternal_aunt(self, mock_get_maternal_grandmother):
        
        self.member.mother = Member(3, "Mom", "Female")

        # check if get_paternal_grandmother has been replaced by a Mock instance
        self.assertEqual(isinstance(self.member.get_maternal_grandmother, Mock), True)
    
        # check for None values
        self.assertEqual(self.member.get_maternal_aunt(), [])
        self.assertEqual(self.member.get_maternal_aunt(), [])
        self.assertEqual(self.member.get_maternal_aunt(), [])
        self.assertEqual(self.member.get_maternal_aunt(), [])

        maternal_aunts = self.member.get_maternal_aunt()
        self.assertEqual(len(maternal_aunts), 1)
        self.assertEqual(maternal_aunts[0].name, "Aunt")
        self.assertEqual(maternal_aunts[0].gender, Gender.female)

        # check that the mock_get_maternal_grandmother is called instead of self.member.get_paternal_grandmother
        mock_get_maternal_grandmother.assert_called_with()

    @patch('family_tree.member.Member.get_maternal_grandmother', side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[Member(3, "Mom", "Female")]),
        create_fake_member(children=[
          Member(3, "Mom", "Female"),
          Member(20, "Aunt", "Female")  
        ]),
        create_fake_member(children=[
          Member(3, "Mom", "Female"),
          Member(19, "Uncle", "Male"),
          Member(20, "Aunt", "Female")
        ])
    ])
    def test_get_maternal_uncle(self, mock_get_maternal_grandmother):

        # check if get_maternal_grandmother has been replaced by a Mock instance
        self.assertEqual(isinstance(self.member.get_maternal_grandmother, Mock), True)
    
        # check for None values
        self.assertEqual(self.member.get_maternal_uncle(), [])
        self.assertEqual(self.member.get_maternal_uncle(), [])
        self.assertEqual(self.member.get_maternal_uncle(), [])
        self.assertEqual(self.member.get_maternal_uncle(), [])

        maternal_uncles = self.member.get_maternal_uncle()
        self.assertEqual(len(maternal_uncles), 1)
        self.assertEqual(maternal_uncles[0].name, "Uncle")
        self.assertEqual(maternal_uncles[0].gender, Gender.male)

        # check that the mock_get_paternal_grandmother is called instead of self.member.get_paternal_grandmother
        mock_get_maternal_grandmother.assert_called_with()

    @patch('family_tree.member.Member.get_spouse_mother', side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children = [Member(7, "Spouse", "Female")]),
        create_fake_member(children = [
            Member(7, "Spouse", "Female"),
            Member(21, "Daughter", "Female")
        ]),
        create_fake_member(children = [
           Member(7, "Spouse", "Female"),
           Member(21, "Daughter", "Female"),
           Member(22, "Son", "Male")
        ])
    ])
    def test_get_brother_in_law(self, mock_get_spouse_mother):

        self.member.spouse = Member(7, "Spouse", "Female")

        # check if get_spouse_mother has been replaced by a Mock instance
        self.assertEqual(isinstance(self.member.get_spouse_mother, Mock), True)

        # check for None values
        self.assertEqual(self.member.get_brother_in_law(), [])
        self.assertEqual(self.member.get_brother_in_law(), [])
        self.assertEqual(self.member.get_brother_in_law(), [])
        self.assertEqual(self.member.get_brother_in_law(), [])

        spouse_brothers = self.member.get_brother_in_law()
        self.assertEqual(len(spouse_brothers), 1)
        self.assertEqual(spouse_brothers[0].name, "Son")
        self.assertEqual(spouse_brothers[0].gender, Gender.male)

        # check that the mock_get_spouse_mother is called instead of self.member.get_spouse_mother
        mock_get_spouse_mother.assert_called_with()

    @patch('family_tree.member.Member.get_spouse_mother', side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children = [Member(7, "Spouse", "Female")]),
        create_fake_member(children = [
            Member(7, "Spouse", "Female"),
            Member(22, "Son", "Male")
        ]),
        create_fake_member(children = [
           Member(7, "Spouse", "Female"),
           Member(21, "Daughter", "Female"),
           Member(22, "Son", "Male")
        ])
    ])
    def test_get_sister_in_law(self, mock_get_spouse_mother):

        self.member.spouse = Member(7, "Spouse", "Female")

        # check if get_spouse_mother has been replaced by a Mock instance
        self.assertEqual(isinstance(self.member.get_spouse_mother, Mock), True)

        # check for None values
        self.assertEqual(self.member.get_sister_in_law(), [])
        self.assertEqual(self.member.get_sister_in_law(), [])
        self.assertEqual(self.member.get_sister_in_law(), [])
        self.assertEqual(self.member.get_sister_in_law(), [])

        spouse_sisters = self.member.get_sister_in_law()
        self.assertEqual(len(spouse_sisters), 1)
        self.assertEqual(spouse_sisters[0].name, "Daughter")
        self.assertEqual(spouse_sisters[0].gender, Gender.female)

        # check that the mock_get_spouse_mother is called instead of self.member.get_spouse_mother
        mock_get_spouse_mother.assert_called_with()

    def test_get_son(self):
        member = Member(23, "Dummy", "Male")
        son = Member(24, "Son", "Male")
        daughter = Member(25, "Daughter", "Female")

        self.assertEqual(member.get_son(), [])
        
        member.children.append(daughter)
        self.assertEqual(member.get_son(), [])

        member.children.append(son)
        sons = member.get_son()
        self.assertEqual(len(sons), 1)
        self.assertEqual(sons[0].name == "Son", True)
        self.assertEqual(sons[0].gender == Gender.male, True)

    def test_get_daughter(self):
        member = Member(23, "Dummy", "Male")
        son = Member(24, "Son", "Male")
        daughter = Member(25, "Daughter", "Female")

        self.assertEqual(member.get_daughter(), [])
        
        member.children.append(son)
        self.assertEqual(member.get_daughter(), [])

        member.children.append(daughter)
        daughters = member.get_daughter()
        self.assertEqual(len(daughters), 1)
        self.assertEqual(daughters[0].name == "Daughter", True)
        self.assertEqual(daughters[0].gender, Gender.female, True)

    def test_get_siblings(self):
        member = Member(23, "Dummy", "Male")
        mother = Member(26, "Mother", "Female")
        son = Member(24, "Son", "Male")
        daughter = Member(25, "Daughter", "Female")

        self.assertEqual(member.get_siblings(), [])

        member.mother = mother
        self.assertEqual(member.get_siblings(), [])

        mother.children.extend([member, son, daughter])

        siblings = member.get_siblings()
        self.assertEqual(len(siblings), 2)





    
    
    