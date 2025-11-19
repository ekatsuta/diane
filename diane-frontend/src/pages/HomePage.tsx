import { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { CheckSquare, Calendar, ShoppingCart, Sparkles, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import { useUserStore } from '@/stores/userStore';

const HomePage = () => {
  const navigate = useNavigate();
  const user = useUserStore((state) => state.user);
  const [quickInput, setQuickInput] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Get current date
  const currentDate = new Date();
  const dateStr = currentDate.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  // Get time of day greeting with user name
  const hour = currentDate.getHours();
  const timeGreeting = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening';
  const userName = user?.first_name || user?.email?.split('@')[0] || '';
  const greeting = `${timeGreeting}, ${userName}`;

  // Mock AI processing logic to determine task complexity
  const handleQuickCapture = async (e: FormEvent) => {
    e.preventDefault();

    if (!quickInput.trim()) return;

    setIsSubmitting(true);

    // Simulate API call delay
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Mock logic to determine if this should be broken into subtasks
    const input = quickInput.toLowerCase();
    const hasMultipleItems =
      input.includes(',') || input.includes(' and ') || input.includes('then');
    const isLongInput = quickInput.length > 60;
    const shouldCreateSubtasks = hasMultipleItems || isLongInput;

    if (shouldCreateSubtasks) {
      // Count approximate number of subtasks based on commas, "and", or length
      const commaCount = (input.match(/,/g) || []).length;
      const andCount = (input.match(/ and /g) || []).length;
      const subtaskCount = Math.max(Math.min(commaCount + andCount + 1, 6), 3);

      toast.success(`Task created with ${subtaskCount} subtasks`, {
        description:
          'We broke down your big task to make it more manageable. Check your Tasks view to review and edit.',
        duration: 5000,
      });
    } else {
      toast.success('Task created', {
        description: 'Your task has been added to your list.',
        duration: 3000,
      });
    }

    setQuickInput('');
    setIsSubmitting(false);
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8 text-left">
        <p className="text-sm text-warm-gray mb-2 uppercase tracking-widest">{dateStr}</p>
        <h1 className="text-5xl mb-3 text-charcoal">{greeting}</h1>
        <p className="text-lg text-charcoal-light">Capture what's on your mind.</p>
      </div>

      {/* Brain Dump Input */}
      <Card className="mb-12 p-8 border-2 border-line-warm shadow-none bg-paper-white rounded-lg text-left">
        <form onSubmit={handleQuickCapture}>
          <div className="mb-4">
            <div className="flex items-center gap-3 mb-2">
              <Sparkles className="w-5 h-5 text-terracotta flex-shrink-0" />
              <label className="text-xs text-warm-gray uppercase tracking-widest">
                Quick Capture
              </label>
            </div>
            <Textarea
              value={quickInput}
              onChange={(e) => setQuickInput(e.target.value)}
              placeholder="Plan birthday party for Noa, buy groceries, schedule dentist appointment..."
              className="border-0 bg-transparent px-0 focus-visible:ring-0 resize-none min-h-[80px] w-full"
              rows={3}
            />
          </div>
          <p className="text-xs text-warm-gray italic mb-4">
            This is a prototype. Full AI functionality coming soon.
          </p>
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Capture'}
          </Button>
        </form>
      </Card>

      {/* Collections Grid */}
      <div className="mb-16">
        <h2 className="text-2xl mb-6 text-charcoal">Your Collections</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          <button
            onClick={() => navigate('/tasks')}
            className="group p-8 border-2 border-line-warm bg-paper-cream hover:border-terracotta transition-all text-left rounded-lg"
          >
            <CheckSquare className="w-8 h-8 mb-4 text-terracotta" strokeWidth={1.5} />
            <h3 className="text-xl mb-2 text-charcoal">Tasks</h3>
            <p className="text-sm text-charcoal-light">Track your to-dos and projects</p>
          </button>

          <button
            onClick={() => navigate('/shopping')}
            className="group p-8 border-2 border-line-warm bg-paper-cream hover:border-sage transition-all text-left rounded-lg"
          >
            <ShoppingCart className="w-8 h-8 mb-4 text-sage" strokeWidth={1.5} />
            <h3 className="text-xl mb-2 text-charcoal">Shopping</h3>
            <p className="text-sm text-charcoal-light">Your grocery & shopping lists</p>
          </button>

          <button
            onClick={() => navigate('/calendar')}
            className="group p-8 border-2 border-line-warm bg-paper-cream hover:border-blush transition-all text-left rounded-lg"
          >
            <Calendar className="w-8 h-8 mb-4 text-terracotta-light" strokeWidth={1.5} />
            <h3 className="text-xl mb-2 text-charcoal">Calendar</h3>
            <p className="text-sm text-charcoal-light">Events and important dates</p>
          </button>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
