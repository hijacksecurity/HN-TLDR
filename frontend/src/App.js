import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Box,
  Chip,
  CircularProgress,
  Alert,
  AppBar,
  Toolbar,
  IconButton,
} from '@mui/material';
import { Refresh as RefreshIcon } from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';

// In Kubernetes, the frontend should use the internal service URL
// When accessed via browser, we need to check if we're in the cluster or not
const API_URL = window.location.hostname === 'localhost'
  ? 'http://localhost:7000'  // Local development/testing
  : `http://${window.location.hostname}:7000`;  // Production with LoadBalancer

function formatTime(timestamp) {
  const date = new Date(timestamp * 1000);
  const now = new Date();
  const diff = Math.floor((now - date) / 1000);

  if (diff < 60) return `${diff}s ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}

function StoryCard({ story, index }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.1 }}
      whileHover={{ scale: 1.02 }}
    >
      <Card
        sx={{
          mb: 2,
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          '&:hover': {
            boxShadow: '0 6px 12px rgba(0, 0, 0, 0.15)',
          }
        }}
      >
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="start" mb={1}>
            <Typography variant="h6" component="h2" sx={{ fontWeight: 600, lineHeight: 1.3 }}>
              {story.title}
            </Typography>
            <Chip
              label={`#${index + 1}`}
              color="primary"
              size="small"
              sx={{ ml: 1, minWidth: 40 }}
            />
          </Box>

          <Typography variant="body1" color="text.secondary" paragraph>
            {story.summary}
          </Typography>

          <Box display="flex" gap={1} flexWrap="wrap" alignItems="center">
            <Chip
              label={`👍 ${story.score}`}
              variant="outlined"
              size="small"
            />
            <Chip
              label={`💬 ${story.descendants}`}
              variant="outlined"
              size="small"
            />
            <Chip
              label={`👤 ${story.by}`}
              variant="outlined"
              size="small"
            />
            <Chip
              label={formatTime(story.time)}
              variant="outlined"
              size="small"
            />
          </Box>
        </CardContent>

        <CardActions>
          {story.url && (
            <Button
              variant="contained"
              color="primary"
              href={story.url}
              target="_blank"
              rel="noopener noreferrer"
              sx={{ mr: 1 }}
            >
              Read Original 📖
            </Button>
          )}
          <Button
            variant="outlined"
            href={`https://news.ycombinator.com/item?id=${story.id}`}
            target="_blank"
            rel="noopener noreferrer"
          >
            HN Comments 💬
          </Button>
        </CardActions>
      </Card>
    </motion.div>
  );
}

function App() {
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchStories = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_URL}/tldr`);
      setStories(response.data.stories);
      setLastUpdated(new Date(response.data.generated_at));
    } catch (err) {
      setError('Failed to fetch stories. Please try again later.');
      console.error('Error fetching stories:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStories();
  }, []);

  return (
    <Box sx={{ flexGrow: 1, minHeight: '100vh' }}>
      <AppBar position="static" sx={{ mb: 4 }}>
        <Toolbar>
          <Typography variant="h5" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
            📰 HackerNews TLDR
          </Typography>
          <IconButton color="inherit" onClick={fetchStories} disabled={loading}>
            <RefreshIcon />
          </IconButton>
        </Toolbar>
      </AppBar>

      <Container maxWidth="md">
        <Box textAlign="center" mb={4}>
          <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 600 }}>
            Top 25 Stories, Summarized
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Get the gist of HackerNews without the time commitment! 🚀
          </Typography>
          {lastUpdated && (
            <Typography variant="caption" display="block" sx={{ mt: 1 }}>
              Last updated: {lastUpdated.toLocaleString()}
            </Typography>
          )}
        </Box>

        <AnimatePresence>
          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <Box display="flex" justifyContent="center" my={4}>
                <CircularProgress size={60} />
              </Box>
            </motion.div>
          )}

          {error && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
            >
              <Alert severity="error" sx={{ mb: 4 }}>
                {error}
              </Alert>
            </motion.div>
          )}

          {!loading && !error && stories.length > 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.3 }}
            >
              {stories.map((story, index) => (
                <StoryCard key={story.id} story={story} index={index} />
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        <Box textAlign="center" mt={4} mb={2}>
          <Typography variant="body2" color="text.secondary">
            Made with ❤️ for the HN community
          </Typography>
        </Box>
      </Container>
    </Box>
  );
}

export default App;
