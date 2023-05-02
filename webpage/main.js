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
const goodsID = document.querySelector('#item-id');
const selectUser = document.querySelector('#discord-id');
const goodsIDContainer = document.querySelector('#item-id-container');

form.addEventListener('submit', (e) => e.preventDefault());

btnSubmitItems.addEventListener('click', (e) => {
	const selectedUser = selectUser.value;
	console.log(selectedUser);
	console.log(IDS[selectedUser]);
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
