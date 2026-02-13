// Use the following command to compile to this file to .js:
// tsc tl-scaffolded-writing.ts --lib es2015,dom --removeComments --downlevelIteration

// You may also need to run this command the first time:
// npm install --no-package-lock @types/jquery @types/jqueryui

type CFG = {
    start: string;
    productions: Production[];
};

type Production = {
    lhs: string;
    rhs: RhsSymbol[];
};

type RhsSymbol = {
    text: string;
    isTerminal: boolean;
};

type PdaConfig = {
    stack: RhsSymbol[];
    remainingInput: string[]; // list in reverse order
};

type SortKey = "ascending" | "descending" | "none";
const Sort = {
    "ascending" : (a: string,b: string) => a < b ? -1 : a > b ? 1 : 0,
    "descending" : (a: string,b: string) => a < b ? 1 : a > b ? -1 : 0
};

const SENTINEL_TOKEN = '$';

function getAllTerminals(cfg: CFG): Set<string> {
    const terminals: Set<string> = new Set();

    for (const production of cfg.productions) {
        for (const symbol of production.rhs) {
            if (symbol.isTerminal) {
                terminals.add(symbol.text);
            }
        }
    }

    return terminals;
}

function getPossibleNextTokens(input: string[], cfg: CFG): Set<string> {
    const possible_next_tokens: Set<string> = new Set();

    const configs_to_explore: PdaConfig[] = [{
        stack: [{ text: SENTINEL_TOKEN, isTerminal: true }, { text: cfg.start, isTerminal: false }],
        remainingInput: input.slice().reverse()
    }];

    while (configs_to_explore.length > 0) {
        const curr_config = configs_to_explore.shift()!;

        if (curr_config.stack.length === 0) {
            continue; // stack is empty so we can't get a next token from this thread
        }

        const curr_symbol = curr_config.stack.pop()!;

        if (curr_symbol.isTerminal) {
            if (curr_config.remainingInput.length === 0) {
                possible_next_tokens.add(curr_symbol.text);

            } else {
                const next_token = curr_config.remainingInput.pop();
                if (curr_symbol.text === next_token) {
                    configs_to_explore.push(curr_config);
                }
            }

        } else { // nonterminal, add all of its production rules
            cfg.productions
                .filter(prod => prod.lhs === curr_symbol.text)
                .forEach(prod => configs_to_explore.push({
                    stack: curr_config.stack.concat(prod.rhs.slice().reverse()),
                    remainingInput: curr_config.remainingInput.slice(),
                }));
        }
    }

    return possible_next_tokens;
}

$(() => {
    // need to wrap button in span in order to display tooltip when button is disabled
    // see here: https://getbootstrap.com/docs/4.0/components/tooltips/#disabled-elements

    $('.question-grade').removeClass('mr-1').wrap('<span class="mr-1">').parent().tooltip({
        // @ts-ignore
        title: "You cannot submit because your response is currently incomplete.",
        placement: "bottom"
    });
});

function capitalizeFirstLetter(s: string): string {
    return s.charAt(0).toUpperCase() + s.slice(1);
}

function setUpScaffoldedWritingQuestion(question_name: string, initial_tokens: string[], cfg: CFG, editable: boolean, sort: SortKey = "none") {
    let entered_tokens = [...initial_tokens];

    function updateNextTokenList() {
        const next_token_list = $('#possible-next-tokens');
        const no_more_tokens_message = $('#no-more-tokens-message');

        next_token_list.empty();

        const possible_next_tokens = getPossibleNextTokens(entered_tokens, cfg);

        if (possible_next_tokens.has(SENTINEL_TOKEN)) {
            possible_next_tokens.delete(SENTINEL_TOKEN);
            enableSubmit();
        } else {
            disableSubmit();
        }

        const should_capitalize = entered_tokens.length === 0 ||
            entered_tokens[entered_tokens.length - 1] === '.';

        let possible_next_tokens_list = Array.from(possible_next_tokens.values());
        if (sort !== "none") {
            possible_next_tokens_list.sort(Sort[sort]);
        }
        for (const token of possible_next_tokens_list) {
            $('<a/>')
                .addClass('badge badge-dark mr-3 my-2')
                .css('cursor', 'pointer')
                .html(should_capitalize ? capitalizeFirstLetter(token) : token)
                .appendTo(next_token_list)
                .on('click', () => {
                    entered_tokens.push(token);
                    handleTokenEnteredOrDeleted();
                });
        }

        if (possible_next_tokens.size === 0) {
            no_more_tokens_message.show();
        } else {
            no_more_tokens_message.hide();
        }
    }

    function assembleResponse(): string {
        const response: string[] = [];

        for (const token of entered_tokens) {
            const should_capitalize = response.length === 0 ||
                response[response.length - 1] === '.';

            if (response.length > 0 && token !== ',' && token !== '.') {
                response.push(' ')
            }

            if (should_capitalize) {
                response.push(capitalizeFirstLetter(token))
            } else {
                response.push(token)
            }
        }

        return response.join('')
    }

    function handleTokenEnteredOrDeleted() {
        // remove spaces before commas and periods
        $('#sentence').html(assembleResponse());

        // the autograder will read the JSON from this hidden input field
        $('input#token-list-json').val(JSON.stringify(entered_tokens));

        // disable "Delete" and "Clear" buttons if response is currently empty
        $('#delete-last-token, #clear-response').prop('disabled', entered_tokens.length === 0);

        updateNextTokenList();
    }

    function disableSubmit() {
        // need to define a class instead of using disabled attribute to avoid interfering with gradeRateMinutes
        // https://prairielearn.readthedocs.io/en/latest/assessment/#limiting-the-rate-at-which-answers-can-be-graded
        // https://github.com/PrairieLearn/PrairieLearn/blob/master/pages/partials/questionFooter.ejs#L155
        $('.question-grade')
            .addClass('tl-scaffolded-writing-incomplete')
            .parent()
            .tooltip('enable');
    }

    const enableSubmit = () => {
        // TODO: If there are multiple scaffolded-writing elements in a single question, then ALL of them
        // must be complete before we enable the overall question to be submitted.
        $('.question-grade')
            .removeClass('tl-scaffolded-writing-incomplete')
            .parent()
            .tooltip('disable');
    }

    // initialize everything when the document is ready
    $(handleTokenEnteredOrDeleted);

    if (!editable){
        return;
    }

    $('#delete-last-token').on('click', () => {
        entered_tokens.pop();
        handleTokenEnteredOrDeleted();
    });

    $('#clear-response').on('click', () => {
        if (window.confirm('Are you sure you want to clear your response?')) {
            entered_tokens = [];
            handleTokenEnteredOrDeleted();
        }
    });
}
