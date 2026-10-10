from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from types import SimpleNamespace
from unittest.mock import patch

from django.core.cache.backends.locmem import LocMemCache
from django.test import SimpleTestCase

from django_visit_count.utils import is_new_visit


class VisitCountTests(SimpleTestCase):
    def setUp(self):
        self.cache = LocMemCache(self.id(), {})
        self.cache.clear()
        self.request = SimpleNamespace(user=SimpleNamespace(is_authenticated=True, id=7))
        self.obj = SimpleNamespace(pk=42)
        cache_patch = patch("django_visit_count.utils.cache", self.cache)
        cache_patch.start()
        self.addCleanup(cache_patch.stop)
        self.addCleanup(self.cache.clear)

    def test_repeated_visit_is_not_new(self):
        self.assertTrue(is_new_visit(self.request, self.obj))
        self.assertFalse(is_new_visit(self.request, self.obj))

    def test_visitors_and_objects_are_independent(self):
        other_request = SimpleNamespace(user=SimpleNamespace(is_authenticated=True, id=8))
        other_obj = SimpleNamespace(pk=43)

        self.assertTrue(is_new_visit(self.request, self.obj))
        self.assertTrue(is_new_visit(other_request, self.obj))
        self.assertTrue(is_new_visit(self.request, other_obj))
        self.assertFalse(is_new_visit(self.request, self.obj))

    def test_anonymous_visits_are_deduplicated(self):
        request = SimpleNamespace(
            user=SimpleNamespace(is_authenticated=False),
            COOKIES={"_ga": "visitor-1"},
            META={"REMOTE_ADDR": "192.0.2.1"},
        )

        self.assertTrue(is_new_visit(request, self.obj))
        self.assertFalse(is_new_visit(request, self.obj))
        request.COOKIES["_ga"] = "visitor-2"
        self.assertTrue(is_new_visit(request, self.obj))

    def test_visit_is_new_after_session_expires(self):
        with patch("time.time", return_value=100):
            self.assertTrue(is_new_visit(self.request, self.obj, session_duration=10))
        with patch("time.time", return_value=105):
            self.assertFalse(is_new_visit(self.request, self.obj, session_duration=10))
        with patch("time.time", return_value=111):
            self.assertTrue(is_new_visit(self.request, self.obj, session_duration=10))

    def test_concurrent_visits_count_only_once(self):
        barrier = Barrier(2)
        original_get = self.cache.get

        def simultaneous_get(*args, **kwargs):
            value = original_get(*args, **kwargs)
            barrier.wait(timeout=5)
            return value

        # Let both requests read the missing key before either can write it,
        # reproducing the race in a separate read followed by a write.
        with patch.object(self.cache, "get", side_effect=simultaneous_get):
            with ThreadPoolExecutor(max_workers=2) as executor:
                results = list(executor.map(lambda _: is_new_visit(self.request, self.obj), range(2)))

        self.assertEqual(sorted(results), [False, True])
