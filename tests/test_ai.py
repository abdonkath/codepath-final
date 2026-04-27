import json
from unittest.mock import MagicMock, patch
from knowledge_base import retrieve
from agent import suggest_tasks


# ── helpers ───────────────────────────────────────────────────────────────────

MOCK_TASKS = [
    {
        "name": "Morning Walk",
        "category": "Exercise",
        "duration_minutes": 30,
        "priority": 5,
        "time": "07:00",
        "recurring": True,
        "interval_days": 1,
    },
    {
        "name": "Ear Cleaning",
        "category": "Health",
        "duration_minutes": 10,
        "priority": 4,
        "time": "09:00",
        "recurring": True,
        "interval_days": 7,
    },
]


def make_mock_response(text):
    msg = MagicMock()
    msg.content = [MagicMock(text=text)]
    return msg


# ── knowledge base tests ──────────────────────────────────────────────────────

def test_retrieve_dog_general_contains_care_info():
    result = retrieve("dog")
    assert "exercise" in result.lower() or "walk" in result.lower() or "vet" in result.lower()


def test_retrieve_golden_retriever_includes_breed_specific():
    result = retrieve("dog", "golden retriever")
    assert "golden retriever" in result.lower()


def test_retrieve_is_case_insensitive():
    lower = retrieve("dog", "golden retriever")
    upper = retrieve("Dog", "Golden Retriever")
    assert lower == upper


def test_retrieve_unknown_breed_falls_back_to_general():
    result = retrieve("dog", "unknown breed xyz")
    assert "general" in result.lower() or "dog" in result.lower()
    assert "unknown breed xyz" not in result.lower()


def test_retrieve_unknown_species_falls_back_to_other():
    result = retrieve("fish")
    assert len(result) > 0


def test_retrieve_cat_persian_includes_breed_specific():
    result = retrieve("cat", "persian")
    assert "persian" in result.lower()


# ── agent tests (mocked — no real API calls) ──────────────────────────────────

def test_suggest_tasks_returns_list():
    with patch("agent.client") as mock_client:
        mock_client.messages.create.return_value = make_mock_response(json.dumps(MOCK_TASKS))
        result = suggest_tasks("Pedro", "Dog", "Golden Retriever", 2)
        assert isinstance(result, list)


def test_suggest_tasks_returns_correct_count():
    with patch("agent.client") as mock_client:
        mock_client.messages.create.return_value = make_mock_response(json.dumps(MOCK_TASKS))
        result = suggest_tasks("Pedro", "Dog", "Golden Retriever", 2)
        assert len(result) == len(MOCK_TASKS)


def test_suggest_tasks_has_required_keys():
    required = {"name", "category", "duration_minutes", "priority", "time", "recurring", "interval_days"}
    with patch("agent.client") as mock_client:
        mock_client.messages.create.return_value = make_mock_response(json.dumps(MOCK_TASKS))
        result = suggest_tasks("Pedro", "Dog", "Golden Retriever", 2)
        for task in result:
            assert required.issubset(task.keys())


def test_suggest_tasks_strips_markdown_fences():
    wrapped = f"```json\n{json.dumps(MOCK_TASKS)}\n```"
    with patch("agent.client") as mock_client:
        mock_client.messages.create.return_value = make_mock_response(wrapped)
        result = suggest_tasks("Luna", "Cat", "Persian", 3)
        assert isinstance(result, list)
        assert len(result) == len(MOCK_TASKS)


def test_suggest_tasks_calls_api_with_pet_details():
    with patch("agent.client") as mock_client:
        mock_client.messages.create.return_value = make_mock_response(json.dumps(MOCK_TASKS))
        suggest_tasks("Pedro", "Dog", "Golden Retriever", 2)
        call_args = mock_client.messages.create.call_args
        prompt = call_args.kwargs["messages"][0]["content"]
        assert "Pedro" in prompt
        assert "Golden Retriever" in prompt
