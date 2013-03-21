from hypothesis.specmapper import SpecificationMapper, MissingSpecification
import pytest

def setup_function(fn):
    SpecificationMapper.default_mapper = None
    fn()

def test_can_define_specifications():
    sm = SpecificationMapper()
    sm.define_specification_for("foo", 1)
    assert sm.specification_for("foo") == 1

def test_can_define_specifications_on_the_default():
    sm = SpecificationMapper()
    SpecificationMapper.default().define_specification_for("foo", 1)
    assert sm.specification_for("foo") == 1

class Bar:
    pass

def test_can_define_specifications_for_classes():
    sm = SpecificationMapper()
    sm.define_specification_for(Bar, 1)
    assert sm.specification_for(Bar) == 1
    
def test_can_define_specifications_for_built_in_types():
    sm = SpecificationMapper()
    sm.define_specification_for(Bar, 1)
    assert sm.specification_for(Bar) == 1

def test_can_define_instance_specifications():
    sm = SpecificationMapper()
    sm.define_specification_for_instances(str, lambda _, i: i + "bar")
    assert sm.specification_for("foo") == "foobar"

def test_can_define_instance_specifications_on_the_default():
    sm = SpecificationMapper()
    SpecificationMapper.default().define_specification_for_instances(str, lambda _, i: i + "bar")
    assert sm.specification_for("foo") == "foobar"

def test_can_define_instance_specifications_for_lists():
    sm = SpecificationMapper()
    sm.define_specification_for_instances(list, lambda _, l: len(l))
    assert sm.specification_for([1,2]) == 2

def test_raises_missing_specification_with_no_spec():
    sm = SpecificationMapper()
    with pytest.raises(MissingSpecification):
        sm.specification_for("hi")

def test_can_create_children():
    sm = SpecificationMapper()
    child = sm.new_child_mapper()
    sm.define_specification_for("foo", 1)
    assert child.specification_for("foo") == 1

def test_can_override_in_children():
    sm = SpecificationMapper()
    child = sm.new_child_mapper()
    sm.define_specification_for("foo", 1)
    child.define_specification_for("foo", 2)

    assert sm.specification_for("foo") == 1
    assert child.specification_for("foo") == 2

class ChildMapper(SpecificationMapper):
  pass

def test_does_not_inherit_default():
  assert ChildMapper.default() != SpecificationMapper.default()

  SpecificationMapper.default().define_specification_for("foo", 1)

  with pytest.raises(MissingSpecification):
    ChildMapper.default().specification_for("foo")
