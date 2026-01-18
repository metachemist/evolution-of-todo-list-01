'use client';

import { useState, useEffect } from 'react';
import apiClient from '@/lib/api';
import CreateTaskForm from '@/components/CreateTaskForm';
import TaskItem from '@/components/TaskItem';

interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/api/v1/tasks/');
      setTasks(response.data);
    } catch (err: any) {
      // Handle different error response formats
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else if (Array.isArray(err.response?.data)) {
        // Handle Pydantic validation errors which come as arrays
        const validationErrors = err.response.data;
        const errorMessage = validationErrors.map((e: any) => e.msg).join(', ');
        setError(errorMessage || 'Validation error occurred');
      } else if (typeof err.response?.data === 'object') {
        // Handle other object responses
        setError(JSON.stringify(err.response.data) || 'An error occurred');
      } else {
        setError(err.response?.data || 'Failed to fetch tasks');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleTaskCreated = (newTask: Task) => {
    setTasks([newTask, ...tasks]);
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDeleted = (taskId: number) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
          <p className="mt-2 text-gray-600">Manage your tasks efficiently</p>
        </div>

        {error && (
          <div className="rounded-md bg-red-50 p-4 mb-4">
            <div className="text-sm text-red-700">{error}</div>
          </div>
        )}

        <div className="bg-white shadow overflow-hidden sm:rounded-lg mb-8">
          <div className="px-4 py-5 sm:px-6">
            <h2 className="text-lg leading-6 font-medium text-gray-900">Create New Task</h2>
          </div>
          <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
            <CreateTaskForm onTaskCreated={handleTaskCreated} />
          </div>
        </div>

        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6">
            <h2 className="text-lg leading-6 font-medium text-gray-900">Your Tasks</h2>
          </div>
          <div className="border-t border-gray-200">
            {tasks.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-500">No tasks yet. Create your first task!</p>
              </div>
            ) : (
              <ul className="divide-y divide-gray-200">
                {tasks.map((task) => (
                  <TaskItem
                    key={task.id}
                    task={task}
                    onUpdate={handleTaskUpdated}
                    onDelete={handleTaskDeleted}
                  />
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}