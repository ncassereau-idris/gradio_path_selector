<svelte:options accessors={true} />

<script lang="ts">
	import type { Gradio } from "@gradio/utils";
	import { BlockTitle } from "@gradio/atoms";
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import { tick } from "svelte";

	export let gradio: Gradio<{
		change: never;
		clear_status: LoadingStatus;
	}>;
	export let label = "File explorer";
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value = "";
	export let show_label: boolean;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus | undefined = undefined;

	let copying: boolean = false;

	let path = "";
	let directories = [];

	function handle_change(): void {
		let obj = JSON.parse(value);
		if (obj.status == "download") {
			path = obj.current_path;
			directories = obj.available_directories;
		}
	}

	function click(index: number): void {
		let obj = {
			"current_path": path,
			"selected_directory": index > -1 ? directories[index] : -1,
			"status": "upload",
		}
		value = JSON.stringify(obj)
		gradio.dispatch("change");
	}

	function copy(): void {
		// Copy the text inside the text field
		navigator.clipboard.writeText(path);
		if (!copying) {
			copying = true
			setTimeout(() => {
				if (copying) copying = false;
			}, 1000);
		}
	}

	$: if (value === null) value = "";

	// When the value changes, dispatch the change event via handle_change()
	// See the docs for an explanation: https://svelte.dev/docs/svelte-components#script-3-$-marks-a-statement-as-reactive
	$: value, handle_change();


</script>

<Block
	{visible}
	{elem_id}
	{elem_classes}
	{scale}
	{min_width}
	allow_overflow={false}
	padding={true}
>
	{#if loading_status}
		<StatusTracker
			autoscroll={gradio.autoscroll}
			i18n={gradio.i18n}
			{...loading_status}
			on:clear_status={() => gradio.dispatch("clear_status", loading_status)}
		/>
	{/if}

	<BlockTitle {show_label} info={undefined}>{label}</BlockTitle>

	<div class="parent">
		<div
			class="scroll-hide path_box"
		>{path}</div>
		<button
			class="submit_btn lg secondary svelte-cmf5ev"
			on:click={copy}
		>
		<div class="copy_icon">
			<svg class="clippy_icon" viewBox="0 0 16 16" class:copying>
				<path class="path1" d="M5.75 4.75H10.25V1.75H5.75V4.75Z" />
				<path class="path2" d="M3.25 2.88379C2.9511 3.05669 2.75 3.37987 2.75 3.75001V13.25C2.75 13.8023 3.19772 14.25 3.75 14.25H12.25C12.8023 14.25 13.25 13.8023 13.25 13.25V3.75001C13.25 3.37987 13.0489 3.05669 12.75 2.88379" />
			</svg>
			<svg class="check_icon" viewBox="0 0 16 16" class:copying>
				<path d="M13.25 4.75L6 12L2.75 8.75" />
			</svg>
		</div>
		</button>
	</div>

	<div class="directories">
		<div
			class="directory_option"
			role="button"
			on:click={() => click(-1)}
			on:keypress={() => click(-1)}
			tabindex="0"
			>
			Up
		</div>
		{#each directories as directory, i}
			<div
				class="directory_option"
				role="button"
				on:click={() => click(i)}
				on:keypress={() => click(i)}
				tabindex="0"
			>
				{directory}
			</div>
		{/each}

	</div>

</Block>

<style>
	*,
	*:after,
	*:before{
		-webkit-box-sizing: border-box;
		-moz-box-sizing: border-box;
		box-sizing: border-box;
	}

	.parent {
		display: grid;
	    grid-template-columns: 4fr minmax(max-content, 1fr);
		grid-column-gap: min(20px, 5vw);
	}

	.path_box {
		position: relative;
		outline: none !important;
		box-shadow: var(--input-shadow);
		background: var(--input-background-fill);
		padding: var(--input-padding);
		width: 100%;
		color: var(--body-text-color);
		font-weight: var(--input-text-weight);
		font-size: var(--input-text-size);
		line-height: var(--line-sm);
		border: var(--input-border-width) solid var(--input-border-color);
		border-radius: 10px;
	}

	.parent>* {
		display: inline-block
	}

	.submit_btn {
		display: flex;
		width: 100%;
		align-items: center;
  		justify-content: center;
	}

	.copy_icon {
		display: block;
		position: relative;
		height: 16px;
		width: 16px;
	}

	.copy_icon>svg {
		position: absolute;
		width: inherit;
		height: inherit;
		fill: "none";
		stroke: white;
		stroke-width: "1.5";
		stroke-linecap: "round";
		stroke-linejoin: "round";

	}
	.copy_icon::after {
		position: absolute;
		content: "Copy path";
		left: 16px;
	}

	svg.clippy_icon {
		fill: grey;
		color: white;
		top: 0;
		left: 0;
		opacity: 1;
		stroke-dasharray: 50;
		stroke-dashoffset: 0;
		transition: all 300ms ease-in-out;
		stroke-width: 1.5;
		stroke-opacity: 1;
	}
	.path2 {
		fill-opacity: 0.3;
	}
	svg.check_icon {
		fill: green;
		top: 0;
		left: 0;
		opacity: 0;
		stroke-dasharray: 50;
		stroke-dashoffset: -50;
		stroke-width: 1.5;
		transition: all 300ms ease-in-out;
	}
	svg.clippy_icon.copying {
		stroke-dashoffset: -50;
		opacity: 0;
	}
	svg.check_icon.copying {
		stroke-dashoffset: 0;
		opacity: 1;
	}

	.directories {
		border-radius: 5px;
		border-width: 2px;
		border-color: grey;
		max-height: 300px;
		overflow-y: scroll;
		margin-top: 1em;
	}

	.directory_option {
		padding-left: 5px;
		padding-top: auto;
		padding-bottom: auto;
		border-color: grey;
		border-width: 1px;
		background-color: #555555;
		transition: background-color 0.2s ease-in-out;
	}

	.directory_option:hover {
		background-color: #198754 ;
	}
</style>
