<!--
Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import { ref } from 'vue'
import CmkDropdown from '@/components/CmkDropdown.vue'
import CmkDropdownButton from '@/components/CmkDropdownButton.vue'

defineProps<{ screenshotMode: boolean }>()

const defaultSelected = ref<string>('init')
const defaultSelected2 = ref<string>('init')
const defaultEmpty1 = ref<string | null>(null)
const defaultEmpty2 = ref<string | null>(null)
const defaultEmpty3 = ref<string | null>(null)
</script>

<template>
  <h2>single element, selected</h2>
  <CmkDropdown
    v-model:selected-option="defaultSelected2"
    :options="{ type: 'fixed', suggestions: [{ name: 'init', title: 'single element' }] }"
    input-hint="some input hint"
    no-results-hint="no results hint"
    component-id="some component id"
    required-text="required"
    label="some label"
  />
  <h2>two elements, selected</h2>
  <CmkDropdown
    v-model:selected-option="defaultSelected"
    :options="{
      type: 'fixed',
      suggestions: [
        { name: 'init', title: 'selected by default' },
        { name: '2', title: 'two' }
      ]
    }"
    input-hint="some input hint"
    no-results-hint="no results hint"
    component-id="some component id"
    required-text="required"
    label="some label"
  />
  <h2>two elements, empty selection</h2>
  <CmkDropdown
    v-model:selected-option="defaultEmpty1"
    :options="{
      type: 'fixed',
      suggestions: [
        { name: '1', title: 'one' },
        { name: '2', title: 'two' }
      ]
    }"
    input-hint="some input hint"
    no-results-hint="no results hint"
    component-id="some component id"
    label="some label"
  />
  <h2>two elements, empty selection, disabled</h2>
  <CmkDropdown
    v-model:selected-option="defaultEmpty1"
    :disabled="true"
    :options="{
      type: 'fixed',
      suggestions: [
        { name: '1', title: 'one' },
        { name: '2', title: 'two' }
      ]
    }"
    input-hint="some input hint"
    no-results-hint="no results hint"
    component-id="some component id"
    label="some label"
  />
  <h2>no elements, empty selection</h2>
  <CmkDropdown
    v-model:selected-option="defaultEmpty2"
    :options="{ type: 'filtered', suggestions: [] }"
    input-hint="some input hint"
    no-results-hint="no results hint"
    component-id="some component id"
    required-text="required"
    label="some label"
  />
  <h2>many elements, filtered, empty selection</h2>
  <CmkDropdown
    v-model:selected-option="defaultEmpty3"
    :options="{
      type: 'filtered',
      suggestions: [
        ...Array(20)
          .fill(0)
          .map((_, i) => ({ name: i.toString(), title: i.toString() }))
      ]
    }"
    input-hint="long dropdown"
    no-results-hint="no results hint"
    component-id="some component id"
    required-text="required"
    label="some label"
  />

  <h1>CmkDropdownButton</h1>
  <h2>button</h2>
  <CmkDropdownButton>default button</CmkDropdownButton>
  <h2>group</h2>
  <CmkDropdownButton group="start">start</CmkDropdownButton
  ><CmkDropdownButton group="end">end</CmkDropdownButton>
</template>
