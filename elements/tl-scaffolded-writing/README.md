### `tl-scaffolded-writing` element

The Scaffolded Writing element allows you to define a context-free grammar, and have students click on tokens to generate sentances, which can be later parsed & graded.

The Scaffolded Writing element was originally written by [Jason Xia][jasonxia17], and has been maintained by the rest of the [TheorieLearn][TheorieLearn] team.

#### Sample element

```html
<tl-scaffolded-writing answers-name="q1">
</tl-scaffolded-writing>
```


#### Customizations

| Attribute | Type | Default | Description |
| --------- | ---- | ------- | ----------- |
| `answers-name` | string | — | Variable name to store data in. Note that this attribute has to be unique within a question, i.e., no value for this attribute should be repeated within a question. |
| `type` | string  | `"DP"` | Display a certain type of example response. Acceptable values are: `"DP" \| "graph"`|
| `sort` | string  | `"none"` | Sort the tokens at each level. Acceptable values are: `"none" \| "ascending" \| "descending"` |


## Details
A CFG has to be provided as a JSON String in the `data["params"]` dictionary. The parameter entry must have the suffix `"*_cfg"`, e.g. `"dp_statement_cfg"`. This element does not *grade* student submissions. It provides the parse tree of the student's submissions, and it is left up to the question writer to determine how much partical credit to give.

TheorieLearn has examples of complex CFGs and constraint-based graders to grade submissions, however are specfific to DP and Graph type questions.

The Scaffolded Writing element is meant to be a single-element question. It is not recommended to place multiple instances of the scaffolding writing element in one question.

[jasonxia17]: https://github.com/jasonxia17
[TheorieLearn]: https://theorielearn.github.io/
