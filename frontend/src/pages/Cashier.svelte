<script lang="ts">
  import { API_URL } from '../api'

  type MenuItem = { menu_item_id: number; menu_item_name: string; price: number }
  type Employee = { employee_id: number; first_name: string; last_name: string; role: string }
  type Line = { item: MenuItem; qty: number }
  type TipChoice = 0 | 0.1 | 0.15 | 0.2

  const EMPLOYEE_KEY = 'cashier.employeeId'
  const MAX_QTY = 99

  let menuItems: MenuItem[] = $state([])
  let employees: Employee[] = $state([])
  let employeeId: number | null = $state(readStoredEmployee())
  let lines: Line[] = $state([])
  let tipRate: TipChoice = $state(0)
  let loadError = $state('')
  let submitError = $state('')
  let submitting = $state(false)
  let lastOrder: { id: number; total: number } | null = $state(null)

  let subtotal = $derived(lines.reduce((sum, l) => sum + l.item.price * l.qty, 0))
  let tip = $derived(Math.round(subtotal * tipRate * 100) / 100)
  let total = $derived(subtotal + tip)
  let itemCount = $derived(lines.reduce((n, l) => n + l.qty, 0))
  let canCharge = $derived(lines.length > 0 && employeeId !== null && !submitting)

  const money = (n: number) => `$${n.toFixed(2)}`

  function readStoredEmployee(): number | null {
    try {
      const v = Number(localStorage.getItem(EMPLOYEE_KEY))
      return v > 0 ? v : null
    } catch {
      return null
    }
  }

  $effect(() => {
    try {
      if (employeeId) localStorage.setItem(EMPLOYEE_KEY, String(employeeId))
    } catch {
      // storage unavailable; selection just won't persist
    }
  })

  async function load() {
    loadError = ''
    try {
      const [menuRes, empRes] = await Promise.all([
        fetch(`${API_URL}/api/menu-items`),
        fetch(`${API_URL}/api/employees`),
      ])
      if (!menuRes.ok || !empRes.ok) throw new Error(`HTTP ${menuRes.status}/${empRes.status}`)
      const items: MenuItem[] = (await menuRes.json()) ?? []
      menuItems = items.sort((a, b) => a.menu_item_name.localeCompare(b.menu_item_name))
      employees = (await empRes.json()) ?? []
      if (employeeId && !employees.some((e) => e.employee_id === employeeId)) employeeId = null
    } catch (err) {
      loadError = `Couldn't load the menu (${err}).`
    }
  }

  $effect(() => {
    load()
  })

  function add(item: MenuItem) {
    lastOrder = null
    submitError = ''
    const line = lines.find((l) => l.item.menu_item_id === item.menu_item_id)
    if (line) line.qty = Math.min(MAX_QTY, line.qty + 1)
    else lines.push({ item, qty: 1 })
  }

  function change(line: Line, delta: number) {
    line.qty += delta
    if (line.qty <= 0) remove(line)
    else line.qty = Math.min(MAX_QTY, line.qty)
  }

  function remove(line: Line) {
    lines = lines.filter((l) => l !== line)
  }

  function clearTicket() {
    lines = []
    tipRate = 0
    submitError = ''
  }

  function qtyInCart(item: MenuItem): number {
    return lines.find((l) => l.item.menu_item_id === item.menu_item_id)?.qty ?? 0
  }

  async function charge() {
    if (!canCharge) return
    submitting = true
    submitError = ''
    try {
      const res = await fetch(`${API_URL}/api/orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          employee_id: employeeId,
          tip,
          items: lines.map((l) => ({ menu_item_id: l.item.menu_item_id, quantity: l.qty })),
        }),
      })
      const body = await res.json().catch(() => ({}))
      if (!res.ok) throw new Error(body.error ?? `HTTP ${res.status}`)
      lastOrder = { id: body.sale_id, total: body.subtotal + body.tip }
      clearTicket()
    } catch (err) {
      submitError = `Order not saved: ${err instanceof Error ? err.message : err}`
    } finally {
      submitting = false
    }
  }

  const tipChoices: { label: string; rate: TipChoice }[] = [
    { label: 'No tip', rate: 0 },
    { label: '10%', rate: 0.1 },
    { label: '15%', rate: 0.15 },
    { label: '20%', rate: 0.2 },
  ]
</script>

<div class="cashier flex min-h-0 flex-1 flex-col gap-3 py-3">
  <header class="flex flex-wrap items-center gap-4">
    <h1 class="text-2xl font-semibold text-primary-dark">Register</h1>
    <label class="ml-auto flex items-center gap-2 text-sm text-muted">
      Cashier
      <select
        class="min-h-12 rounded border border-line bg-surface px-3 text-base text-ink focus-visible:outline-2 focus-visible:outline-primary"
        bind:value={employeeId}
      >
        <option value={null} disabled>Select…</option>
        {#each employees as e (e.employee_id)}
          <option value={e.employee_id}>{e.first_name} {e.last_name}</option>
        {/each}
      </select>
    </label>
  </header>

  {#if loadError}
    <div role="alert" class="flex items-center gap-3 rounded border border-red-300 bg-red-50 p-3 text-red-800">
      {loadError}
      <button type="button" class="btn ml-auto" onclick={load}>Retry</button>
    </div>
  {/if}

  <div class="flex min-h-0 flex-1 gap-4">
    <!-- Menu -->
    <section aria-label="Menu" class="min-h-0 flex-1 overflow-y-auto">
      <div class="grid grid-cols-[repeat(auto-fill,minmax(150px,1fr))] gap-3">
        {#each menuItems as item (item.menu_item_id)}
          {@const qty = qtyInCart(item)}
          <button
            type="button"
            class={[
              'btn relative flex min-h-24 flex-col items-start justify-between gap-2 p-3 text-left active:bg-highlight/30',
              qty > 0 && 'border-primary bg-highlight/10',
            ]}
            onclick={() => add(item)}
            aria-label="Add {item.menu_item_name}, {money(item.price)}{qty ? `, ${qty} in order` : ''}"
          >
            <span class="font-semibold leading-tight">{item.menu_item_name}</span>
            <span class="text-muted tabular-nums">{money(item.price)}</span>
            {#if qty > 0}
              <span
                aria-hidden="true"
                class="absolute top-2 right-2 grid size-7 place-items-center rounded-full bg-primary text-sm font-bold text-white"
              >
                {qty}
              </span>
            {/if}
          </button>
        {/each}
      </div>
    </section>

    <!-- Ticket -->
    <aside aria-label="Current order" class="flex w-96 shrink-0 flex-col rounded border border-line bg-surface">
      <div class="flex items-center justify-between border-b border-line px-4 py-3">
        <h2 class="text-lg font-semibold">Order</h2>
        <span class="text-muted">{itemCount} {itemCount === 1 ? 'item' : 'items'}</span>
      </div>

      <ul class="min-h-0 flex-1 divide-y divide-line overflow-y-auto">
        {#each lines as line (line.item.menu_item_id)}
          <li class="flex items-center gap-2 px-3 py-2">
            <div class="min-w-0 flex-1">
              <div class="truncate font-medium">{line.item.menu_item_name}</div>
              <div class="text-sm text-muted tabular-nums">{money(line.item.price)} ea</div>
            </div>
            <button
              type="button"
              class="btn size-12 p-0 text-xl"
              aria-label="Remove one {line.item.menu_item_name}"
              onclick={() => change(line, -1)}>−</button
            >
            <span class="w-8 text-center text-lg font-semibold tabular-nums" aria-label="Quantity">{line.qty}</span>
            <button
              type="button"
              class="btn size-12 p-0 text-xl"
              aria-label="Add one {line.item.menu_item_name}"
              onclick={() => change(line, 1)}>+</button
            >
            <span class="w-16 text-right font-semibold tabular-nums">{money(line.item.price * line.qty)}</span>
          </li>
        {:else}
          <li class="p-6 text-center text-muted">
            {#if lastOrder}
              <span role="status" class="text-primary-dark">
                Order #{lastOrder.id} saved — {money(lastOrder.total)}
              </span>
            {:else}
              Tap items to start an order
            {/if}
          </li>
        {/each}
      </ul>

      <div class="space-y-3 border-t border-line p-4">
        <fieldset class="grid grid-cols-4 gap-2" disabled={lines.length === 0}>
          <legend class="mb-1 text-sm text-muted">Tip</legend>
          {#each tipChoices as choice}
            <button
              type="button"
              aria-pressed={tipRate === choice.rate}
              class={[
                'btn min-h-12 px-1 disabled:opacity-40',
                tipRate === choice.rate && 'bg-primary text-white hover:bg-primary',
              ]}
              onclick={() => (tipRate = choice.rate)}>{choice.label}</button
            >
          {/each}
        </fieldset>

        <dl class="space-y-1 tabular-nums">
          <div class="flex justify-between text-muted"><dt>Subtotal</dt><dd>{money(subtotal)}</dd></div>
          <div class="flex justify-between text-muted"><dt>Tip</dt><dd>{money(tip)}</dd></div>
          <div class="flex justify-between text-xl font-bold"><dt>Total</dt><dd>{money(total)}</dd></div>
        </dl>

        {#if submitError}
          <p role="alert" class="rounded bg-red-50 p-2 text-sm text-red-800">{submitError}</p>
        {/if}
        {#if employeeId === null && lines.length > 0}
          <p class="text-sm text-amber-700">Select a cashier before charging.</p>
        {/if}

        <div class="flex gap-2">
          <button
            type="button"
            class="btn min-h-14 disabled:opacity-40"
            onclick={clearTicket}
            disabled={lines.length === 0 || submitting}>Clear</button
          >
          <button
            type="button"
            class="min-h-14 flex-1 cursor-pointer rounded bg-primary text-lg font-semibold text-white hover:bg-primary-dark focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary disabled:cursor-not-allowed disabled:opacity-40"
            onclick={charge}
            disabled={!canCharge}
          >
            {submitting ? 'Saving…' : `Charge ${money(total)}`}
          </button>
        </div>
      </div>
    </aside>
  </div>
</div>
