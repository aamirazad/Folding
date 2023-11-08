export async function load({ fetch }) {
	const user_count = await fetch('https://api.foldingathome.org/user-count');

	return {
		user_count: await user_count.text()
	};
}