def test_gemini_provider_config():
    import config
    assert config.LLM_PROVIDER in {"gemini", "openai", "ollama"}
    assert config.GEMINI_MODEL
