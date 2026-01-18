import { useState } from 'react';
import apiClient from '@/lib/api';
import { TrashIcon, CheckCircleIcon, CircleIcon } from 'lucide-react';

interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface TaskItemProps {
  task: Task;
  onUpdate: (updatedTask: Task) => void;
  onDelete: (taskId: number) => void;
}

export default function TaskItem({ task, onUpdate, onDelete }: TaskItemProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);

  const handleToggleCompletion = async () => {
    try {
      setIsUpdating(true);
      const response = await apiClient.patch(`/api/v1/tasks/${task.id}/complete`);
      onUpdate(response.data);
    } catch (err) {
      console.error('Failed to update task:', err);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      setIsDeleting(true);
      await apiClient.delete(`/api/v1/tasks/${task.id}`);
      onDelete(task.id);
    } catch (err) {
      console.error('Failed to delete task:', err);
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <li className="px-4 py-4 sm:px-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <button
            onClick={handleToggleCompletion}
            disabled={isUpdating}
            className={`mr-3 ${isUpdating ? 'opacity-50 cursor-not-allowed' : 'hover:opacity-75'}`}
          >
            {task.completed ? (
              <CheckCircleIcon className="h-5 w-5 text-green-500" />
            ) : (
              <CircleIcon className="h-5 w-5 text-gray-400" />
            )}
          </button>
          <div>
            <h3 className={`text-sm font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`text-sm ${task.completed ? 'line-through text-gray-500' : 'text-gray-500'}`}>
                {task.description}
              </p>
            )}
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
            {new Date(task.created_at).toLocaleDateString()}
          </span>
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className={`${isDeleting ? 'opacity-50 cursor-not-allowed' : 'text-red-600 hover:text-red-900'}`}
          >
            <TrashIcon className="h-5 w-5" />
          </button>
        </div>
      </div>
    </li>
  );
}