var __values = (this && this.__values) || function(o) {
    var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
    if (m) return m.call(o);
    if (o && typeof o.length === "number") return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
    throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};
var __read = (this && this.__read) || function (o, n) {
    var m = typeof Symbol === "function" && o[Symbol.iterator];
    if (!m) return o;
    var i = m.call(o), r, ar = [], e;
    try {
        while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
    }
    catch (error) { e = { error: error }; }
    finally {
        try {
            if (r && !r.done && (m = i["return"])) m.call(i);
        }
        finally { if (e) throw e.error; }
    }
    return ar;
};
var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};
var Sort = {
    "ascending": function (a, b) { return a < b ? -1 : a > b ? 1 : 0; },
    "descending": function (a, b) { return a < b ? 1 : a > b ? -1 : 0; }
};
var SENTINEL_TOKEN = '$';
function getAllTerminals(cfg) {
    var e_1, _a, e_2, _b;
    var terminals = new Set();
    try {
        for (var _c = __values(cfg.productions), _d = _c.next(); !_d.done; _d = _c.next()) {
            var production = _d.value;
            try {
                for (var _e = (e_2 = void 0, __values(production.rhs)), _f = _e.next(); !_f.done; _f = _e.next()) {
                    var symbol = _f.value;
                    if (symbol.isTerminal) {
                        terminals.add(symbol.text);
                    }
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
                }
                finally { if (e_2) throw e_2.error; }
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return terminals;
}
function getPossibleNextTokens(input, cfg) {
    var possible_next_tokens = new Set();
    var configs_to_explore = [{
            stack: [{ text: SENTINEL_TOKEN, isTerminal: true }, { text: cfg.start, isTerminal: false }],
            remainingInput: input.slice().reverse()
        }];
    var _loop_1 = function () {
        var curr_config = configs_to_explore.shift();
        if (curr_config.stack.length === 0) {
            return "continue";
        }
        var curr_symbol = curr_config.stack.pop();
        if (curr_symbol.isTerminal) {
            if (curr_config.remainingInput.length === 0) {
                possible_next_tokens.add(curr_symbol.text);
            }
            else {
                var next_token = curr_config.remainingInput.pop();
                if (curr_symbol.text === next_token) {
                    configs_to_explore.push(curr_config);
                }
            }
        }
        else {
            cfg.productions
                .filter(function (prod) { return prod.lhs === curr_symbol.text; })
                .forEach(function (prod) { return configs_to_explore.push({
                stack: curr_config.stack.concat(prod.rhs.slice().reverse()),
                remainingInput: curr_config.remainingInput.slice(),
            }); });
        }
    };
    while (configs_to_explore.length > 0) {
        _loop_1();
    }
    return possible_next_tokens;
}
$(function () {
    $('.question-grade').removeClass('mr-1').wrap('<span class="mr-1">').parent().tooltip({
        title: "You cannot submit because your response is currently incomplete.",
        placement: "bottom"
    });
});
function capitalizeFirstLetter(s) {
    return s.charAt(0).toUpperCase() + s.slice(1);
}
function setUpScaffoldedWritingQuestion(question_name, initial_tokens, cfg, editable, sort) {
    if (sort === void 0) { sort = "none"; }
    var entered_tokens = __spreadArray([], __read(initial_tokens), false);
    function updateNextTokenList() {
        var e_3, _a;
        var next_token_list = $('#possible-next-tokens');
        var no_more_tokens_message = $('#no-more-tokens-message');
        next_token_list.empty();
        var possible_next_tokens = getPossibleNextTokens(entered_tokens, cfg);
        if (possible_next_tokens.has(SENTINEL_TOKEN)) {
            possible_next_tokens.delete(SENTINEL_TOKEN);
            enableSubmit();
        }
        else {
            disableSubmit();
        }
        var should_capitalize = entered_tokens.length === 0 ||
            entered_tokens[entered_tokens.length - 1] === '.';
        var possible_next_tokens_list = Array.from(possible_next_tokens.values());
        if (sort !== "none") {
            possible_next_tokens_list.sort(Sort[sort]);
        }
        var _loop_2 = function (token) {
            $('<a/>')
                .addClass('badge badge-dark mr-3 my-2')
                .css('cursor', 'pointer')
                .html(should_capitalize ? capitalizeFirstLetter(token) : token)
                .appendTo(next_token_list)
                .on('click', function () {
                entered_tokens.push(token);
                handleTokenEnteredOrDeleted();
            });
        };
        try {
            for (var possible_next_tokens_list_1 = __values(possible_next_tokens_list), possible_next_tokens_list_1_1 = possible_next_tokens_list_1.next(); !possible_next_tokens_list_1_1.done; possible_next_tokens_list_1_1 = possible_next_tokens_list_1.next()) {
                var token = possible_next_tokens_list_1_1.value;
                _loop_2(token);
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (possible_next_tokens_list_1_1 && !possible_next_tokens_list_1_1.done && (_a = possible_next_tokens_list_1.return)) _a.call(possible_next_tokens_list_1);
            }
            finally { if (e_3) throw e_3.error; }
        }
        if (possible_next_tokens.size === 0) {
            no_more_tokens_message.show();
        }
        else {
            no_more_tokens_message.hide();
        }
    }
    function assembleResponse() {
        var e_4, _a;
        var response = [];
        try {
            for (var entered_tokens_1 = __values(entered_tokens), entered_tokens_1_1 = entered_tokens_1.next(); !entered_tokens_1_1.done; entered_tokens_1_1 = entered_tokens_1.next()) {
                var token = entered_tokens_1_1.value;
                var should_capitalize = response.length === 0 ||
                    response[response.length - 1] === '.';
                if (response.length > 0 && token !== ',' && token !== '.') {
                    response.push(' ');
                }
                if (should_capitalize) {
                    response.push(capitalizeFirstLetter(token));
                }
                else {
                    response.push(token);
                }
            }
        }
        catch (e_4_1) { e_4 = { error: e_4_1 }; }
        finally {
            try {
                if (entered_tokens_1_1 && !entered_tokens_1_1.done && (_a = entered_tokens_1.return)) _a.call(entered_tokens_1);
            }
            finally { if (e_4) throw e_4.error; }
        }
        return response.join('');
    }
    function handleTokenEnteredOrDeleted() {
        $('#sentence').html(assembleResponse());
        $('input#token-list-json').val(JSON.stringify(entered_tokens));
        $('#delete-last-token, #clear-response').prop('disabled', entered_tokens.length === 0);
        updateNextTokenList();
    }
    function disableSubmit() {
        $('.question-grade')
            .addClass('tl-scaffolded-writing-incomplete')
            .parent()
            .tooltip('enable');
    }
    var enableSubmit = function () {
        $('.question-grade')
            .removeClass('tl-scaffolded-writing-incomplete')
            .parent()
            .tooltip('disable');
    };
    $(handleTokenEnteredOrDeleted);
    if (!editable) {
        return;
    }
    $('#delete-last-token').on('click', function () {
        entered_tokens.pop();
        handleTokenEnteredOrDeleted();
    });
    $('#clear-response').on('click', function () {
        if (window.confirm('Are you sure you want to clear your response?')) {
            entered_tokens = [];
            handleTokenEnteredOrDeleted();
        }
    });
}
