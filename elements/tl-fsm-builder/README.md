### `tl-fsm-builder` element

The FSM Builder element provides an interactive interface for constructing finite state machines (FSMs) specifically Deterministic Finite Automata (DFAs) and Nondeterministic Finite Automata (NFAs). It supports grading based on FSM correctness and provides interactive feedback on user submissions.

The FSM Builder element was written by [Eliot Robson][eliotwrobson] and [Sam Ruggerio][Surg-Dev],
along with help from the rest of the [TheorieLearn][TheorieLearn] team. Uses the [automata library][automata-lib]
as the backend for the grading algorithms.

#### Sample element

```html
<tl-fsm-builder answers-name="my-fsm" fsm-type="DFA" weight="2" alphabet="01">
  <tl-correct-answer max-states="6">
    { "final_states": [ "10,odd" ], "initial_state": "e,even", "input_symbols":
    [ "1", "0" ], "states": [ "1,odd", "10,even", "1,even", "10,odd", "e,even",
    "e,odd" ], "transitions": { "1,even": { "0": "10,odd", "1": "1,odd" },
    "1,odd": { "0": "10,even", "1": "1,even" }, "10,even": { "0": "e,odd", "1":
    "1,odd" }, "10,odd": { "0": "e,even", "1": "1,even" }, "e,even": { "0":
    "e,odd", "1": "1,odd" }, "e,odd": { "0": "e,even", "1": "1,even" } } }
  </tl-correct-answer>
</tl-fsm-builder>
```

#### Customizations

| Attribute                 | Type    | Default | Description                                                                                                                                                                                |
| ------------------------- | ------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `answers-name`            | string  | --      | The name of the answer field. This is used to reference the FSM in the grading and submission logic.                                                                                       |
| `fsm-type`                | string  | --      | Specifies the type of finite state machine. Acceptable values are (case-insensitive) `"DFA"` or `"NFA"`.                                                                                   |
| `weight`                  | integer | 1       | The weight or point value for the question. This is used when calculating the overall score for the question.                                                                              |
| `alphabet`                | string  | `"01"`  | A string of characters defining the input alphabet for the FSM. Each character in the string is treated as a separate symbol.                                                              |
| `epsilon-symbol`          | string  | `"e"`   | A character representing epsilon transitions for NFAs. Should not be present in the `alphabet` string, and should only be set if the `fsm-type` is `"NFA"`.                                |
| `max-check-length`        | integer | `10`    | The maximum length of input strings used to generate feedback. This is used to limit the runtime of the feedback generation.                                                               |
| `max-state-score-scaling` | float   | `0.5`   | The scaling factor for the score deduction if there are too many states in the FSM. This is used to penalize students for using too many states in their FSM. Must be between 0.0 and 1.0. |

For the inner `tl-correct-answer` tag:

| Attribute    | Type    | Default | Description                                                                                                                                                             |
| ------------ | ------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `max-states` | integer | —       | Maximum number of states a student submission may contain before receiving a score deduction. Students get half credit for submitting an FSM that goes over this limit. |

#### Details

The `tl-fsm-builder` element accepts a correct answer in JSON format inside the `tl-correct-answer` tag. The student submissions are checked for equivalence with this reference solution, and feedback is given in the case of incorrect answers.

[eliotwrobson]: https://github.com/eliotwrobson
[Surg-Dev]: https://github.com/Surg-Dev
[TheorieLearn]: https://theorielearn.github.io/
[automata-lib]: https://github.com/caleb531/automata
