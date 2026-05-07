import { test } from '../../test';

export default test({
	error: {
		code: 'legacy_export_invalid',
		message: 'Cannot use `export let` in runes mode — use `$props()` instead'
	}
});
