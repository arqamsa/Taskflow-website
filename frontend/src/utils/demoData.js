export const demoUser = { id: 1, name: 'Alex Morgan', email: 'alex@taskflow.local' }

export const demoProjects = [
  { id: 1, name: 'Website refresh', description: 'A sharper public face for the product team.', status: 'ACTIVE', task_count: 6 },
  { id: 2, name: 'Mobile launch', description: 'Coordinate the beta release and feedback loop.', status: 'ACTIVE', task_count: 4 },
  { id: 3, name: 'Team operations', description: 'Small improvements that make work feel lighter.', status: 'ARCHIVED', task_count: 3 },
]

export const demoTasks = [
  { id: 1, title: 'Shape the launch narrative', project_id: 1, project_name: 'Website refresh', status: 'IN_PROGRESS', priority: 'HIGH', due_date: '2026-09-18' },
  { id: 2, title: 'Review analytics events', project_id: 1, project_name: 'Website refresh', status: 'REVIEW', priority: 'MEDIUM', due_date: '2026-09-20' },
  { id: 3, title: 'Prepare beta release notes', project_id: 2, project_name: 'Mobile launch', status: 'TODO', priority: 'CRITICAL', due_date: '2026-09-22' },
  { id: 4, title: 'Send onboarding survey', project_id: 2, project_name: 'Mobile launch', status: 'DONE', priority: 'LOW', due_date: '2026-09-15' },
  { id: 5, title: 'Tighten design tokens', project_id: 1, project_name: 'Website refresh', status: 'DONE', priority: 'MEDIUM', due_date: '2026-09-14' },
]
