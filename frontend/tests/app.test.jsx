import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { BrowserRouter } from 'react-router-dom'
import App from '../src/App'

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
  })

  it('renders the dashboard and sample kanban content when the API is offline', async () => {
    render(<BrowserRouter><App /></BrowserRouter>)
    expect(await screen.findByRole('heading', { name: 'Good morning, Alex.' })).toBeInTheDocument()
    expect(await screen.findByText('Prepare beta release notes')).toBeInTheDocument()
    expect(screen.getByText('Work by status')).toBeInTheDocument()
  })
})
