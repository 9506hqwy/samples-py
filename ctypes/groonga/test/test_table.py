from ctypes_groonga import Context, Groonga, Table
from ctypes_groonga.table import create_table, list_tables

from test import GroongaTestCase


class TestTable(GroongaTestCase):
    def test_list_tables(self) -> None:
        with Groonga(self.lib_path) as g:
            with g.create_ctx(self.db_path) as c:
                tables = list_tables(c)
                self.assertSequenceEqual(tables, [])

    def test_create_table(self) -> None:
        with Groonga(self.lib_path) as g:
            with g.create_ctx(self.db_path) as c:
                table = self._create_table(c)
                self.assertEqual(table.name, "Test")  # type: ignore[attr-defined]

    def test_create_column(self) -> None:
        with Groonga(self.lib_path) as g:
            with g.create_ctx(self.db_path) as c:
                t = self._create_table(c)
                self.assertEqual(len(t.columns), 1)
                t.create_column(name="name", type="ShortText")
                self.assertEqual(len(t.columns), 2)
                self.assertEqual(t.columns[0].name, "_key")  # type: ignore[attr-defined]
                self.assertEqual(t.columns[1].name, "name")  # type: ignore[attr-defined]

    def test_load_delete(self) -> None:
        with Groonga(self.lib_path) as g:
            with g.create_ctx(self.db_path) as c:
                t = self._create_table(c)
                t.create_column(name="name", type="ShortText")

                values = [
                    {
                        "_key": "aaa",
                        "name": "AAA",
                    },
                ]
                ret = t.load(values=values)

                self.assertEqual(ret, len(values))
                self.assertEqual(t.count, 1)

                num, rows = t.select()
                self.assertEqual(num, ret)
                self.assertEqual(len(rows), ret)
                self.assertEqual(rows[0].key, "aaa")  # type: ignore[attr-defined]
                self.assertEqual(rows[0].name, "AAA")  # type: ignore[attr-defined]

                b = t.delete(key="aaa")
                self.assertTrue(b)
                self.assertEqual(t.count, 0)

                num, rows = t.select()
                self.assertEqual(num, 0)
                self.assertEqual(len(rows), 0)

    def test_select_clear(self) -> None:
        with Groonga(self.lib_path) as g:
            with g.create_ctx(self.db_path) as c:
                t = self._create_table(c)
                t.create_column(name="name", type="ShortText")
                n, records = t.select()
                self.assertEqual(n, 0)
                self.assertSequenceEqual(records, [])

                values = self._create_loaddata()
                n = t.load(values=values)
                self.assertEqual(n, len(values))

                n, records = t.select()
                self.assertEqual(n, len(values))
                self.assertEqual(len(records), len(values))

                n, records = t.select(query="_id:1")
                self.assertEqual(n, 1)
                self.assertEqual(records[0].name, "A")  # type: ignore[attr-defined]

                n, records = t.select(query='_key:"aa"')
                self.assertEqual(n, 1)
                self.assertEqual(records[0].name, "AA")  # type: ignore[attr-defined]

                t.clear()

                n, records = t.select()
                self.assertEqual(n, 0)
                self.assertSequenceEqual(records, [])

    def _create_loaddata(self) -> list[dict[str, str]]:
        return [
            {
                "_key": "a",
                "name": "A",
            },
            {
                "_key": "aa",
                "name": "AA",
            },
            {
                "_key": "aaa",
                "name": "AAA",
            },
            {
                "_key": "aaaa",
                "name": "AAAA",
            },
        ]

    def _create_table(self, ctx: Context) -> Table:
        d = {
            "name": "Test",
            "flags": "TABLE_HASH_KEY",
            "key_type": "ShortText",
        }
        return create_table(ctx, **d)
