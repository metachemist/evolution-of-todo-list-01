import { useState } from 'react';
import { useRouter } from 'next/navigation';
import apiClient from '@/lib/api';
import { TrashIcon, CheckCircleIcon, CircleIcon, Pencil, Check, X } from 'lucide-react';

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
  onRefresh?: () => void; // Optional for refresh after save
}

export default function TaskItem({ task, onUpdate, onDelete, onRefresh }: TaskItemProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description);
  const router = useRouter();

  const handleToggleCompletion = async () => {
    try {
      setIsUpdating(true);
      const response = await apiClient.patch(`/api/v1/tasks/${task.id}/complete`);
      onUpdate(response.data);
    } catch (err: any) {
      // Handle 401 errors by redirecting to login
      if (err.response?.status === 401) {
        router.push('/login');
        return;
      }
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
    } catch (err: any) {
      // Handle 401 errors by redirecting to login
      if (err.response?.status === 401) {
        router.push('/login');
        return;
      }
      console.error('Failed to delete task:', err);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleSave = async () => {
    try {
      setIsUpdating(true);
      const response = await apiClient.put(`/api/v1/tasks/${task.id}`, {
        title: editTitle,
        description: editDescription
      });
      onUpdate(response.data);
      setIsEditing(false);
      if (onRefresh) {
        onRefresh(); // Trigger parent to reload if provided
      }
    } catch (err: any) {
      // Handle 401 errors by redirecting to login
      if (err.response?.status === 401) {
        router.push('/login');
        return;
      }
      console.error('Failed to update task:', err);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleCancel = () => {
    setEditTitle(task.title);
    setEditDescription(task.description);
    setIsEditing(false);
  };

  return (
    <li className="px-4 py-4 sm:px-6 border-b border-border">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <button
            onClick={handleToggleCompletion}
            disabled={isUpdating || isEditing}
            className={`mr-3 ${isUpdating || isEditing ? 'opacity-50 cursor-not-allowed' : 'hover:opacity-75'}`}
          >
            {task.completed ? (
              <CheckCircleIcon className="h-5 w-5 text-green-500 dark:text-green-400" />
            ) : (
              <CircleIcon className="h-5 w-5 text-muted-foreground" />
            )}
          </button>
          <div className="flex-1 min-w-0">
            {isEditing ? (
              <>
                <input
                  type="text"
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  className="block w-full p-2 mb-2 text-sm border border-border rounded-md shadow-sm focus:ring-accent focus:border-accent bg-background text-foreground"
                  placeholder="Task title"
                />
                <textarea
                  value={editDescription}
                  onChange={(e) => setEditDescription(e.target.value)}
                  className="block w-full p-2 text-sm border border-border rounded-md shadow-sm focus:ring-accent focus:border-accent bg-background text-foreground"
                  placeholder="Task description"
                  rows={3}
                />
              </>
            ) : (
              <>
                <h3 className={`text-sm font-medium ${task.completed ? 'line-through text-muted-foreground' : 'text-foreground'}`}>
                  {task.title}
                </h3>
                {task.description && (
                  <p className={`text-sm ${task.completed ? 'line-through text-muted-foreground' : 'text-muted-foreground'}`}>
                    {task.description}
                  </p>
                )}
              </>
            )}
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-secondary text-secondary-foreground">
            {new Date(task.created_at).toLocaleDateString()}
          </span>

          {!isEditing ? (
            <button
              onClick={() => {
                setIsEditing(true);
                setEditTitle(task.title);
                setEditDescription(task.description);
              }}
              disabled={isUpdating || isDeleting}
              className={`${(isUpdating || isDeleting) ? 'opacity-50 cursor-not-allowed' : 'text-accent hover:text-accent-foreground'}`}
            >
              <Pencil className="h-5 w-5" />
            </button>
          ) : null}

          {isEditing && (
            <>
              <button
                onClick={handleSave}
                disabled={isUpdating}
                className={`${isUpdating ? 'opacity-50 cursor-not-allowed' : 'text-green-600 hover:text-green-500 dark:text-green-400 dark:hover:text-green-300'}`}
              >
                <Check className="h-5 w-5" />
              </button>
              <button
                onClick={handleCancel}
                disabled={isUpdating}
                className={`${isUpdating ? 'opacity-50 cursor-not-allowed' : 'text-destructive hover:text-destructive-foreground'}`}
              >
                <X className="h-5 w-5" />
              </button>
            </>
          )}

          {!isEditing && (
            <button
              onClick={handleDelete}
              disabled={isDeleting}
              className={`${isDeleting ? 'opacity-50 cursor-not-allowed' : 'text-destructive hover:text-destructive-foreground'}`}
            >
              <TrashIcon className="h-5 w-5" />
            </button>
          )}
        </div>
      </div>
    </li>
  );
}