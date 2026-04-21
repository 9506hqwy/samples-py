from pathlib import Path

from ctypes_groonga import Groonga, error

from test import GroongaTestCase


class TestGroonga(GroongaTestCase):
    def test_init_fin(self) -> None:
        with Groonga(self.lib_path):
            pass

    def test_encoding(self) -> None:
        with Groonga(self.lib_path) as g:
            encoding = g.encoding
            self.assertIsNotNone(encoding)

            g.encoding = "sjis"
            encoding = g.encoding
            self.assertEqual(encoding, "sjis")

    def test_version(self) -> None:
        with Groonga(self.lib_path) as g:
            self.assertIsNotNone(g.version)

    def test_ctx_create_close(self) -> None:
        with Groonga(self.lib_path) as g:
            with g.create_ctx(self.db_path) as ctx:
                c = ctx.ctx
                self.assertEqual(c.rc, 0)
                self.assertEqual(c.encoding, 3)  # UTF-8
                self.assertEqual(c.errline, 0)
                self.assertIsNone(c.user_data)
                self.assertEqual(c.errfile, b"")
                self.assertEqual(c.errfunc, b"")
                self.assertEqual(c.errbuf, b"")

    def test_send_recv_at_create_and_open(self) -> None:
        with Groonga(self.lib_path) as g:
            with g.create_ctx(self.db_path) as c:
                r = c.send("status")
                self.assertEqual(r, 0)

                d = c.recv()
                self.assertIsNotNone(d)

            with g.open_ctx(self.db_path) as c:
                r = c.send("status")
                self.assertEqual(r, 0)

                d = c.recv()
                self.assertIsNotNone(d)

    def test_send_recv_at_tmp(self) -> None:
        with Groonga(self.lib_path) as g:
            with g.create_ctx(None) as c:
                r = c.send("status")
                self.assertEqual(r, 0)

                d = c.recv()
                self.assertIsNotNone(d)

    def test_grn_fin_twice(self) -> None:
        with self.assertRaisesRegex(Exception, "grn_fin"):
            with Groonga(self.lib_path) as g:
                g.fin()

    def test_ctx_create_not_exist(self) -> None:
        with Groonga(self.lib_path) as g:
            with self.assertRaisesRegex(Exception, "grn_db_create"):
                g.create_ctx(Path("/a/a/a"))

    def test_ctx_open_not_exist(self) -> None:
        with Groonga(self.lib_path) as g:
            with self.assertRaisesRegex(Exception, "grn_db_open"):
                g.open_ctx(Path("aaa"))

    def test_ctx_close_twice(self) -> None:
        with Groonga(self.lib_path) as g:
            with g.create_ctx(None) as c:
                pass

            with self.assertRaisesRegex(Exception, "grn_ctx_db"):
                g.close_ctx(c)

    def test_send_unknown_command(self) -> None:
        with Groonga(self.lib_path) as g:
            with g.create_ctx(None) as c:
                with self.assertRaisesRegex(error.GroongaError, "invalid command name: unknown"):
                    c.send("unknown")
