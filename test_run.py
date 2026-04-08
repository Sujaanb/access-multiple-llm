import json
from util.llm_factory import LLMFactory
from util.cache_and_cost import CacheManager
from util.system_prompt import prompt_generate_summary


def generate_summary(text):
    """
    Generates a summary of the given text using the LLM.
    """
    response = LLMFactory.invoke(
        system_prompt=prompt_generate_summary,
        human_message=text,
        temperature=0.7,
        local_llm=False,
        use_cache=True,  # Enable caching
    )
    summary = response.content.strip()
    return summary


def demonstrate_caching():
    """
    Demonstrate caching in action by making the same query twice.
    The second query will use the cache instead of hitting the API.
    """
    question = "What is the impact of climate change in global trade?"
    
    print("=" * 70)
    print("🔄 FIRST CALL - This will hit the API (no cache)")
    print("=" * 70)
    summary1 = generate_summary(question)
    print(f"\n📝 Summary:\n{summary1}\n")
    
    print("=" * 70)
    print("💾 SECOND CALL - This will use the cache (no API call)")
    print("=" * 70)
    summary2 = generate_summary(question)
    print(f"\n📝 Summary (from cache):\n{summary2}\n")
    
    # Verify both summaries are identical
    assert summary1 == summary2, "Summaries should be identical!"
    print("✅ Both summaries match perfectly!\n")
    
    # Display cost summary
    print("=" * 70)
    print("💰 COST TRACKING SUMMARY")
    print("=" * 70)
    cache_manager = CacheManager()
    cost_summary = cache_manager.get_cost_summary()
    
    print(f"\n📊 Total API Cost: ${cost_summary['total_cost']}")
    if cost_summary['providers']:
        print("\nBreakdown by provider:")
        for provider, data in cost_summary['providers'].items():
            print(f"  • {provider.upper()}:")
            print(f"    - Total Cost: ${data['total_cost']:.6f}")
            print(f"    - Total Tokens: {data['total_tokens']}")
            print(f"    - API Calls Made: {data['num_calls']}")
    print()


if __name__ == "__main__":
    demonstrate_caching()
