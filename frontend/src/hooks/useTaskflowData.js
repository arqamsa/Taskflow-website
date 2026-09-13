import { useCallback, useEffect, useState } from 'react'
import { dashboardApi, projectApi, taskApi } from '../services/api'
import { demoProjects, demoTasks } from '../utils/demoData'

export function useTaskflowData() {
  const [projects, setProjects] = useState([])
  const [tasks, setTasks] = useState([])
  const [dashboard, setDashboard] = useState(null)
  const [usingDemo, setUsingDemo] = useState(false)

  const refresh = useCallback(async () => {
    try {
      const [projectResponse, taskResponse, dashboardResponse] = await Promise.all([projectApi.list(), taskApi.list(), dashboardApi.get()])
      setProjects(projectResponse.data)
      setTasks(taskResponse.data)
      setDashboard(dashboardResponse.data)
      setUsingDemo(false)
    } catch {
      setProjects(demoProjects)
      setTasks(demoTasks)
      setDashboard({ total_projects: 3, total_tasks: 5, completed_tasks: 2, pending_tasks: 3, tasks_by_status: { TODO: 1, IN_PROGRESS: 1, REVIEW: 1, DONE: 2 }, tasks_by_priority: { LOW: 1, MEDIUM: 2, HIGH: 1, CRITICAL: 1 }, recent_tasks: demoTasks })
      setUsingDemo(true)
    }
  }, [])

  useEffect(() => { refresh() }, [refresh])

  const changeTaskStatus = async (taskId, status) => {
    setTasks((items) => items.map((task) => task.id === taskId ? { ...task, status } : task))
    if (!usingDemo) await taskApi.update(taskId, { status })
  }

  return { projects, tasks, dashboard, usingDemo, refresh, changeTaskStatus }
}
