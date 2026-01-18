import { useState } from 'react';
import { useRouter } from 'next/navigation';
import apiClient from '@/lib/api';

interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface CreateTaskFormProps {
  onTaskCreated: (newTask: Task) => void;
}

export default function CreateTaskForm({ onTaskCreated }: CreateTaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    try {
      setIsSubmitting(true);
      setError('');

      const response = await apiClient.post('/api/v1/tasks/', {
        title: title.trim(),
        description: description.trim(),
        completed: false,
      });

      onTaskCreated(response.data);
      setTitle('');
      setDescription('');
    } catch (err: any) {
      // Handle 401 errors by redirecting to login
      if (err.response?.status === 401) {
        router.push('/login');
        return;
      }

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
        setError(err.response?.data || 'Failed to create task');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="rounded-md bg-red-50 p-4 dark:bg-red-950">
          <div className="text-sm text-red-700 dark:text-red-300">{error}</div>
        </div>
      )}

      <div>
        <label htmlFor="title" className="block text-sm font-medium text-foreground">
          Title *
        </label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="mt-1 block w-full px-3 py-2 border border-border rounded-md shadow-sm focus:outline-none focus:ring-accent focus:border-accent sm:text-sm bg-background text-foreground"
          placeholder="Enter task title"
          disabled={isSubmitting}
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-foreground">
          Description
        </label>
        <textarea
          id="description"
          rows={3}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="mt-1 block w-full px-3 py-2 border border-border rounded-md shadow-sm focus:outline-none focus:ring-accent focus:border-accent sm:text-sm bg-background text-foreground"
          placeholder="Enter task description (optional)"
          disabled={isSubmitting}
        />
      </div>

      <div>
        <button
          type="submit"
          disabled={isSubmitting}
          className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-accent-foreground ${
            isSubmitting
              ? 'bg-accent/50 cursor-not-allowed'
              : 'bg-accent hover:bg-accent/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent'
          }`}
        >
          {isSubmitting ? 'Creating...' : 'Create Task'}
        </button>
      </div>
    </form>
  );
}