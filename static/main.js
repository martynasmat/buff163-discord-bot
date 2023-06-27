const IDS = {
	tsitrina: '210699700158988288',
	mmmmmmm: '248428145919787008',
	Durnelis: '212910603327504384',
	Gimzha: '300938639158935552',
	rok: '280744687227109377',
	rokazz: '598398078268997632',
};
const URLs = [];

const form = document.querySelector('#form');
const btnAddItem = document.querySelector('#btn-add');
const btnSubmitItems = document.querySelector('#btn-submit');
const buffURL = document.querySelector('#buff-url');
const selectUser = document.querySelector('#discord-id');
const goodsIDContainer = document.querySelector('#item-id-container');
const profitMargin = document.querySelector('#profit-margin');

form.addEventListener('submit', (e) => e.preventDefault());

btnSubmitItems.addEventListener('click', apiRequest);

btnAddItem.addEventListener('click', () => {
	const url = buffURL.value;
	const margin = profitMargin.value;

	if (!url || !margin) return alert('Prasišviesk galvą');

	const item = {
		url,
		margin,
		pattern: '',
		float: 0,
	}

	URLs.push(item);
	const div = document.createElement('div');
	div.innerText = `${JSON.stringify(item)}`;
	goodsIDContainer.appendChild(div);

	console.log(URLs);

	buffURL.value = '';
	profitMargin.value = '';
});

function apiRequest() {
	if (URLs.length === 0) return alert('Add at least one item to your tracking list before submitting');

	const options = {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': '*',
		},
		// body: JSON.stringify({
		// 	mode: 1,
		// 	arg: buffURL.value,
		// 	float: 0,
		// 	pattern: '',
		// 	discord_id: IDS[selectUser.value],
		// 	margin: profitMargin.value,
		// }),
		body: JSON.stringify({
			mode: 1,
			arg: URLs,
			discord_id: IDS[selectUser.value],
		}),
	};

	fetch('http://127.0.0.1:5000/add-item', options)
		.then((response) => {
			const container = document.querySelectorAll('.notification-container')[0];
			const div = document.createElement('div');
			div.style.backgroundColor = `${
				response.status === 201 ? 'green' : 'red'
			}`;
			div.innerText = `${
				response.status === 201
					? 'Item uploaded to database successfully!'
					: 'Something went wrong, try again.'
			}`;
			container.appendChild(div);

			setTimeout(() => {
				container.removeChild(div);
			}, 5_000);
	});
}