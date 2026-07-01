// Shared political-allocation direction ('D' or 'R') across the two
// interactive tools. Toggling in MapMoves updates MoversBudget in real
// time (and vice versa) so the reader's context is preserved as they
// scroll from one tool to the next.
//
// Prerender-safe: the module instantiates once per SSR render at build
// time and re-initializes cleanly on client hydration. No state can
// leak between page loads.

import { writable } from 'svelte/store';

/** @type {import('svelte/store').Writable<'D' | 'R'>} */
export const direction = writable('D');
