from utils import generate_prompts, generate_queries_and_evaluate_bias


def main(model="gemma:2b", mode_generator='random', n_generator=5):
    g = generate_prompts(mode_generator, n_generator)
    r = generate_queries_and_evaluate_bias(g, model)


if __name__ == '__main__':
    main(model="llama3:8b", n_generator=1)
