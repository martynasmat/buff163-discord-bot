function apiRequest() {
	const xhr = new XMLHttpRequest();
	xhr.open("POST", "http://127.0.0.1:5000/add-item");
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.setRequestHeader("Access-Control-Allow-Origin", '*')
	const body = JSON.stringify({
		mode: 1,
		arg: goodsID.value,
		float: 0,
		pattern: '',
		discord_id: String(IDS[selectUser.options[selectUser.selectedIndex].text]),
		margin: profitMargin.value,
	});
	console.log(IDS[selectUser.options[selectUser.selectedIndex].text]);
	xhr.send(body);
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
const profitMargin = document.querySelector('#profit-margin')

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

	const id = goodsID.value;

	IDlist.add(id);
	const div = document.createElement('div');
	div.innerText = `${id}`;
	goodsIDContainer.appendChild(div);

	console.log(IDlist);

	goodsID.value = '';
});
