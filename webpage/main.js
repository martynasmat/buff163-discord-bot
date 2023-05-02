const IDS = {
	tsitrina: 210699700158988288,
	mmmmmmm: 248428145919787008,
	Durnelis: 212910603327504384,
	Gimzha: 300938639158935552,
	rok: 280744687227109377,
	rokazz: 598398078268997632,
};

const btnAddItem = document.querySelector('#btn-add');
const btnSubmitItems = document.querySelector('#btn-submit');
const selectedID = document.querySelector('#discord-id');

selectedID.addEventListener('change', (e) => {
	const user = e.target.value;
	console.log(IDS[user]);
});
