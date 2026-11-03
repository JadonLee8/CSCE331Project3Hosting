<script lang="ts">
  // Mock data until orders are wired to the backend.
  type TicketItem = {
    name: string
    qty: number
  }

  type Ticket = {
    id: number
    source: 'Kiosk' | 'Cashier' | 'Online'
    type: 'Dine-in' | 'Takeout'
    customer?: string
    placedAt: number
    items: TicketItem[]
  }

  const minutesAgo = (m: number) => Date.now() - m * 60_000

  let tickets: Ticket[] = $state([
    {
      id: 101,
      source: 'Cashier',
      type: 'Dine-in',
      placedAt: minutesAgo(10),
      items: [
        { name: 'Glazed Donut', qty: 2 },
        { name: 'Iced Coffee', qty: 1 },
      ],
    },
    {
      id: 102,
      source: 'Kiosk',
      type: 'Takeout',
      customer: 'Maria',
      placedAt: minutesAgo(5),
      items: [
        { name: 'Boston Cream', qty: 1 },
        { name: 'Chocolate Sprinkle', qty: 3 },
      ],
    },
    {
      id: 103,
      source: 'Online',
      type: 'Takeout',
      customer: 'Jordan',
      placedAt: minutesAgo(2),
      items: [{ name: 'Dozen Assorted', qty: 1 }, { name: 'Hot Latte', qty: 2 }],
    },
  ])

  let lastBumped: Ticket | null = $state(null)
  let now = $state(Date.now())

  $effect(() => {
    const timer = setInterval(() => (now = Date.now()), 1000)
    return () => clearInterval(timer)
  })

  function placedTime(placedAt: number): string {
    return new Date(placedAt).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })
  }

  // Header color by ticket age: green < 5 min, amber < 10 min, red after.
  function ageClass(placedAt: number): string {
    const mins = (now - placedAt) / 60_000
    if (mins < 5) return 'bg-primary'
    if (mins < 10) return 'bg-amber-500'
    return 'bg-red-600'
  }

  function bump(ticket: Ticket) {
    tickets = tickets.filter((t) => t.id !== ticket.id)
    lastBumped = ticket
  }

  function recall() {
    if (!lastBumped) return
    tickets = [...tickets, lastBumped].sort((a, b) => a.placedAt - b.placedAt)
    lastBumped = null
  }

  let clock = $derived(new Date(now).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }))
</script>

<div class="kitchen flex min-h-0 flex-1 flex-col gap-4 py-4">
  <header class="flex items-center gap-4">
    <h1 class="text-2xl font-semibold text-primary-dark">Kitchen</h1>
    <span class="text-muted">{tickets.length} open</span>
    <span class="ml-auto text-xl font-semibold tabular-nums">{clock}</span>
    <button type="button" class="btn min-h-12 disabled:opacity-40" onclick={recall} disabled={!lastBumped}>
      Recall last
    </button>
  </header>

  {#if tickets.length === 0}
    <p class="m-auto text-xl text-muted">No open orders</p>
  {:else}
    <div class="flex min-h-0 flex-1 gap-4 overflow-x-auto pb-2">
      {#each tickets as ticket (ticket.id)}
        <article class="flex w-64 shrink-0 flex-col overflow-hidden rounded border border-line bg-surface shadow-sm">
          <div class="flex items-center justify-between px-3 py-2 text-white {ageClass(ticket.placedAt)}">
            <span class="text-lg font-bold">#{ticket.id}</span>
            <span class="text-lg font-semibold tabular-nums">{placedTime(ticket.placedAt)}</span>
          </div>

          <div class="flex justify-between border-b border-line px-3 py-1 text-sm text-muted">
            <span>{ticket.type} · {ticket.source}</span>
            {#if ticket.customer}<span>{ticket.customer}</span>{/if}
          </div>

          <ul class="flex-1 space-y-2 overflow-y-auto px-3 py-2">
            {#each ticket.items as item}
              <li><span class="font-semibold">{item.qty}×</span> {item.name}</li>
            {/each}
          </ul>

          <button
            type="button"
            class="min-h-14 cursor-pointer border-t border-line bg-canvas text-lg font-semibold text-primary-dark hover:bg-highlight/15 active:bg-highlight/30"
            onclick={() => bump(ticket)}
          >
            Done
          </button>
        </article>
      {/each}
    </div>
  {/if}
</div>
