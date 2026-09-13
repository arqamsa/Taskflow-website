import { describe, expect, it } from 'vitest'
import { completionRate, groupByStatus } from '../src/utils/taskUtils'

describe('task utilities', () => {
  it('calculates completion percentage', () => {
    expect(completionRate(3, 4)).toBe(75)
    expect(completionRate(0, 0)).toBe(0)
  })

  it('groups tasks by workflow status', () => {
    expect(groupByStatus([{ status: 'TODO', id: 1 }, { status: 'DONE', id: 2 }, { status: 'TODO', id: 3 }]).TODO).toHaveLength(2)
  })
})
