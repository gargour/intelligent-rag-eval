from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas.run_config import RunConfig
from datasets import Dataset
from app.evaluation.ragas_config import get_ragas_llm, get_ragas_embeddings

def evaluate_rag_dataset(questions: list, answers: list, contexts: list, ground_truths: list):
    dataset = Dataset.from_dict({
        "user_input": questions,
        "response": answers,
        "retrieved_contexts": contexts,
        "reference": ground_truths,
    })

    llm = get_ragas_llm()
    embeddings = get_ragas_embeddings()

    run_config = RunConfig(max_workers=2, timeout=120)

    result = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=llm,
        embeddings=embeddings,
        run_config=run_config,
    )
    return result.to_pandas()