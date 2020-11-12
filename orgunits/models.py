"""
Copyright 2020 ООО «Верме»
"""

from django.db import models
from django.db.models.expressions import RawSQL


class OrganizationQuerySet(models.QuerySet):
    def tree_downwards(self, root_org_id):
        """
        Возвращает корневую организацию с запрашиваемым root_org_id и всех её детей любого уровня вложенности
        TODO: Написать фильтр с помощью ORM или RawSQL запроса или функций Python

        :type root_org_id: int
        """
        sql = """
            WITH RECURSIVE children AS (
                SELECT id
                FROM orgunits_organization
                WHERE orgunits_organization.id = %s
                UNION
                SELECT orgunits_organization.id
                FROM orgunits_organization
                INNER JOIN children
                ON orgunits_organization.parent_id = children.id
            )
        SELECT * FROM children
        """
        result = RawSQL(sql, [root_org_id])

        return self.filter(id__in=result)

    def tree_upwards(self, child_org_id):
        """
        Возвращает корневую организацию с запрашиваемым child_org_id и всех её родителей любого уровня вложенности
        TODO: Написать фильтр с помощью ORM или RawSQL запроса или функций Python

        :type child_org_id: int
        """
        sql = """
            WITH RECURSIVE parents(id) AS ( 
                SELECT %s
                UNION
                SELECT parent_id
                FROM orgunits_organization , parents
                WHERE orgunits_organization.id = parents.id
                ) 
            SELECT id 
            FROM orgunits_organization
            WHERE orgunits_organization.id in parents
            """
        result = RawSQL(sql, [child_org_id])

        return self.filter(id__in=result)


class Organization(models.Model):
    """ Организаци """

    objects = OrganizationQuerySet.as_manager()

    name = models.CharField(max_length=1000, blank=False, null=False, verbose_name="Название")
    code = models.CharField(max_length=1000, blank=False, null=False, unique=True, verbose_name="Код")
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, verbose_name="Вышестоящая организация",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Организация"
        verbose_name = "Организации"

    def __str__(self):
        return f"{self.name}"

    def parents(self):
        """
        Возвращает всех родителей любого уровня вложенности
        TODO: Написать метод, используя ORM и .tree_upwards()

        :rtype: django.db.models.QuerySet
        """
        result = Organization.objects.tree_upwards(self.id)
        return result.exclude(id=self.id)

    def children(self):
        """
        Возвращает всех детей любого уровня вложенности
        TODO: Написать метод, используя ORM и .tree_downwards()

        :rtype: django.db.models.QuerySet
        """
        result = Organization.objects.tree_downwards(self.id)
        return result.exclude(id=self.id)
