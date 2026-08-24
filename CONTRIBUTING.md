# Contributing

Thanks for helping keep this collection useful and current.

## Suggest a resource

Open a [resource request](https://github.com/sraodev/awesome-opensource-cheat-sheets/issues/new?template=resource.yml) or submit a pull request. One resource per issue or pull request makes review faster.

Include:

- the resource name and canonical URL;
- its category;
- a one-sentence description;
- why it is useful as a quick reference;
- the date you verified it;
- its license or redistribution terms, if proposing a local file.

## Acceptance criteria

A resource must be:

- directly relevant to an open-source tool, project, standard, or practice;
- concise enough to work as a quick reference;
- publicly accessible without requiring an account;
- maintained by its project or a credible community;
- free of affiliate links and unnecessary tracking parameters;
- current, or clearly marked as historical.

Prefer linking to a project-owned, maintained page. Add a PDF to the repository only when its license clearly permits redistribution and the offline copy adds value.

## Pull request checklist

1. Search the README and existing issues for duplicates.
2. Add the entry to the most specific category.
3. Keep the description factual and to one sentence.
4. Confirm every new link opens and every local path matches the file name exactly.
5. Update the README's review date only when you checked all current official links.
6. Explain how you verified any AI-assisted contribution; contributors remain responsible for accuracy and licensing.

The scheduled workflow requires the README and trend report review dates to match and be no more than 120 days old.

Run the repository-owned validation before submitting:

```bash
python3 scripts/validate_collection.py
```

Changes to categorization, descriptions, accessibility, and stale links are welcome. Avoid unrelated formatting or large generated rewrites.

## Community

Be respectful, specific, and constructive. Reviews may ask for stronger sourcing, a narrower change, or clearer licensing before merge.
