### `tl-regex-input` element

The Regex Input element allows you to define a reference NFA as a correct answer, and have students enter in their own regex, and is checked for equivalence. The element will respond with feedback of counterexamples to their regex if it is incorrect.

The Regex input was originally written by [Jason Xia][jasonxia17], and has been maintained by the rest of the [TheorieLearn][TheorieLearn] team. It uses the [automata library][automata-lib]
as the backend for the grading.

#### Sample element

```html
<tl-regex-input answers-name="regex-q1">
001+010+011+100+101+110+111
</tl-regex-input>

<tl-regex-input answers-name="regex-q2" alphabet="abc">
(a+bb*) + (b*a*c*)cc* + cc*(a+b*c)
</tl-regex-input>
```


#### Customizations

| Attribute | Type | Default | Description |
| --------- | ---- | ------- | ----------- |
| `answers-name` | string | — | Variable name to store data in. Note that this attribute has to be unique within a question, i.e., no value for this attribute should be repeated within a question. |
| `weight` | integer | 1 | Weight to use when computing a weighted average score over elements |
| `alphabet` | string | `"01"` | The alphabet string of supported characters. There is no support for multi-character literals |

[jasonxia17]: https://github.com/jasonxia17
[TheorieLearn]: https://theorielearn.github.io/
[automata-lib]: https://github.com/caleb531/automata
