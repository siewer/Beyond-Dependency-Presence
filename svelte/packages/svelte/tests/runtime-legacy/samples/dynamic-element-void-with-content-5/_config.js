import { test } from '../../test';

export default test({
	compileOptions: {
		dev: true
	},
	warnings: ['`<svelte:element this="input">` is a void element — it cannot have content']
});
