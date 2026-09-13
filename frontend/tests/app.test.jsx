import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { BrowserRouter } from 'react-router-dom'
import App from '../src/App'
import { ThemeProvider } from '../src/context/ThemeContext'

vi.mock('../src/services/api', () => ({
  authApi: { login: vi.fn(), register: vi.fn(), me: vi.fn() },
  projectApi: { list: vi.fn(() => Promise.reject(new Error('offline'))), create: vi.fn(), update: vi.fn(), remove: vi.fn() },
  taskApi: { list: vi.fn(() => Promise.reject(new Error('offline'))), create: vi.fn(), update: vi.fn(), remove: vi.fn() },
  dashboardApi: { get: vi.fn(() => Promise.reject(new Error('offline'))) },
}))

describe('TaskFlow workspace', () => {
  beforeEach(() => {
    localStorage.setItem('taskflow_user', JSON.stringify({ name: 'Alex Morgan', email: 'alex@example.com' }))
    localStorage.setItem('taskflow_token', 'test-token')
    localStorage.removeItem('taskflow_theme')
  })

  it('renders the dashboard and sample kanban content when the API is offline', async () => {
    render(<ThemeProvider><BrowserRouter><App /></BrowserRouter></ThemeProvider>)
    expect(await screen.findByRole('heading', { name: 'Good morning, Alex.' })).toBeInTheDocument()
    expect(await screen.findByText('Prepare beta release notes')).toBeInTheDocument()
    expect(screen.getByText('Work by status')).toBeInTheDocument()
  })

  it('toggles and remembers the dark theme', async () => {
    const { userEvent } = await import('@testing-library/user-event')
    const user = userEvent.setup()
    render(<ThemeProvider><BrowserRouter><App /></BrowserRouter></ThemeProvider>)

    const toggle = screen.getByRole('button', { name: 'Switch to dark theme' })
    await user.click(toggle)

    expect(document.documentElement.dataset.theme).toBe('dark')
    expect(localStorage.getItem('taskflow_theme')).toBe('dark')
    expect(screen.getByRole('button', { name: 'Switch to light theme' })).toBeInTheDocument()
  })
})
