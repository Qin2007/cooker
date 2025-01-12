// javascript
"use strict";
const elementById = document.getElementById('elementById');
const jsonic = JSON.parse(document.querySelector('pre[hidden]').innerText);
console.log(JSON.stringify(jsonic, null, 2));

function html_encode(strx) {
    strx = String(strx);
    strx = strx.replace(/&/g, '&amp;');
    strx = strx.replace(/"/g, '&quot;');
    strx = strx.replace(/>/g, '&gt;');
    strx = strx.replace(/</g, '&lt;');
    return strx.replace(/'/g, '&#39;');

}

const tin_s = 1;
const tin_m = 60;
const tin_h = 60 * 60;
const tin_d = (60 * 60) * 24;

/**
 * calculates a human time thing from seconds
 */
function timeDecode(seconds) {
    const else_d = seconds % tin_d;
    const else_h = else_d % tin_h;
    return {
        'ResultS': Math.floor(else_h % tin_m),
        'Minutes': Math.floor(else_h / tin_m),
        'Hours': Math.floor(else_d / tin_h),
        'Days': Math.floor(seconds / tin_d),
    };
}

try {
    elementById.innerHTML = '';
    jsonic.forEach(function (element) {
        let innerHTML = `<li><form action="/edit" method=post><h3>${html_encode(element['title'])}</h3>Aanmaakdatum: `;
        innerHTML += `<time datetime="${html_encode(element['Date'])}">to be determined</time>`;
        const result = timeDecode(Number(element['time']) * 60);
        innerHTML += `<br/>bereidingtijd: ${result['Hours']} Hours, ${result['Minutes']} Minutes, ${result['ResultS']} Seconds`;
        innerHTML += `<input name=uuid value="${html_encode(element['uuid'])}" type=hidden>`;

        innerHTML += `<h3>ingedienten</h3><ol>`;
        const ingredient = [], benodigheid = [];
        Object.entries(element).forEach(function ([element, value]) {
            const exec = /^([a-zA-Z]+)_([0-9]+)$/.exec(String(element));
            if (exec) {
                switch (exec[1]) {
                    case "ingredient":
                        if (ingredient[exec[2]] === undefined) {
                            ingredient[exec[2]] = [value, null];
                        }
                        ingredient[exec[2]][0] = value;
                        break;
                    case "unit":
                        if (ingredient[exec[2]] === undefined) {
                            ingredient[exec[2]] = [null, value];
                        }
                        ingredient[exec[2]][1] = value;
                        break;
                    case"benodigheid":
                        benodigheid[exec[2]] = value;
                        break;
                    default:
                        console.warn(exec[1], 'is not a valid element');
                }
            }
        });
        ingredient.forEach(function (indexedElement) {
            innerHTML += `<li>${html_encode(indexedElement.join(' '))}`;
        });
        innerHTML += '</ol><h3>benodigheden</h3><ol>';
        benodigheid.forEach(function (indexedElement) {
            innerHTML += `<li>${html_encode(indexedElement)}`;
        });
        innerHTML += '</ol><p>to remove a recipe simply remove it from the json file<!--<button type="submit" name="action" value="remove">remove recipe</button>--></form>';
        elementById.innerHTML += innerHTML;
    });
} catch (e) {
    elementById.innerHTML = '<li><p>Your data contains malformed data';
    throw e;
}
document.querySelectorAll('time').forEach(function (each) {
    each.innerText = `${new Date(each.dateTime)}`.replace(/ GMT.+/, '');
});