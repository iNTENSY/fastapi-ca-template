from app.domain.core.entity import DomainEntity


class _TestModelAttr:
    @property
    def model(self) -> DomainEntity:
        raise NotImplementedError

    def test_model_attr(self, field, _type) -> None:
        all_fields = self.model.__annotations__
        assert field in all_fields.keys(), (
            f"В модели `{self.model.__name__}` укажите атрибут `{field}`"
        )
        field_type_into_model = all_fields.get(field)
        assert field_type_into_model == _type, (
            field_type_into_model, _type,
        )
