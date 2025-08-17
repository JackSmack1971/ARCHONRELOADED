"use client"

import { createContext, useContext, useReducer, ReactNode, Dispatch } from 'react'

interface State { count: number }
type Action = { type: 'inc' }

const StoreContext = createContext<{ state: State; dispatch: Dispatch<Action> } | null>(null)

function reducer(state: State, action: Action): State {
  if (action.type === 'inc') return { count: state.count + 1 }
  return state
}

export function StoreProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(reducer, { count: 0 })
  return <StoreContext.Provider value={{ state, dispatch }}>{children}</StoreContext.Provider>
}

export function useStore() {
  const ctx = useContext(StoreContext)
  if (!ctx) throw new Error('StoreProvider missing')
  return ctx
}
