function apiRequest() {
	const options = {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': '*',
		},
		body: JSON.stringify({
			mode: 1,
			arg: goodsID.value,
			float: 0,
			pattern: '',
			discord_id: String(IDS[selectUser.value]),
			margin: profitMargin.value,
		}),
	};
	fetch('http://37.221.93.227:8000/add-item', options).then((response) => {
		const container = document.querySelectorAll(
			'.notification-container'
		)[0];
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
		}, 5000);
	});
}

const IDS = {
	tsitrina: 210699700158988288,
	mmmmmmm: 248428145919787008,
	Durnelis: 212910603327504384,
	Gimzha: 300938639158935552,
	rok: 280744687227109377,
	rokazz: 598398078268997632,
};

const IDlist = new Set();

const form = document.querySelector('#form');
const btnAddItem = document.querySelector('#btn-add');
const btnSubmitItems = document.querySelector('#btn-submit');
const goodsID = document.querySelector('#buff-url');
const selectUser = document.querySelector('#discord-id');
const goodsIDContainer = document.querySelector('#item-id-container');
const profitMargin = document.querySelector('#profit-margin');

form.addEventListener('submit', (e) => e.preventDefault());

btnSubmitItems.addEventListener('click', (e) => {
	const selectedUser = selectUser.value;
	console.log(selectedUser);
	console.log(IDS[selectedUser]);
	apiRequest();
});

btnAddItem.addEventListener('click', () => {
	if (!goodsID.value || IDlist.has(goodsID.value))
		return alert('Prasišviesk galvą');

	// const id = goodsID.value;

	// IDlist.add(id);
	// const div = document.createElement('div');
	// div.innerText = `${id}`;
	// goodsIDContainer.appendChild(div);

	// console.log(IDlist);

	// goodsID.value = '';
});
