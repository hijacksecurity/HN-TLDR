import { render, screen } from '@testing-library/react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import App from './App';

const theme = createTheme({
  palette: {
    primary: {
      main: '#ff6600',
    },
  },
});

const renderWithTheme = (component) => {
  return render(
    <ThemeProvider theme={theme}>
      {component}
    </ThemeProvider>
  );
};

test('renders HackerNews TLDR title', () => {
  renderWithTheme(<App />);
  const titleElement = screen.getByText(/HackerNews TLDR/i);
  expect(titleElement).toBeInTheDocument();
});

test('renders loading state initially', () => {
  renderWithTheme(<App />);
  const loadingElement = screen.getByRole('progressbar');
  expect(loadingElement).toBeInTheDocument();
});

test('renders subtitle text', () => {
  renderWithTheme(<App />);
  const subtitleElement = screen.getByText(/Get the gist of HackerNews without the time commitment/i);
  expect(subtitleElement).toBeInTheDocument();
});
