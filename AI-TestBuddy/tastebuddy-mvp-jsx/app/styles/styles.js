import { StyleSheet } from 'react-native';
import { theme } from './theme';

export const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: theme.colors.background,
    padding: theme.spacing(2),
  },
  title: {
    fontSize: theme.fonts.sizes.xl,
    fontWeight: '800',
    color: theme.colors.text,
    marginBottom: theme.spacing(1),
  },
  subtitle: {
    fontSize: theme.fonts.sizes.md,
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing(2),
  },
  card: {
    backgroundColor: theme.colors.surface,
    padding: theme.spacing(2),
    borderRadius: theme.radius.md,
    borderWidth: 1,
    borderColor: theme.colors.border,
    marginBottom: theme.spacing(2),
  },
  button: {
    backgroundColor: theme.colors.primary,
    borderRadius: theme.radius.md,
    paddingVertical: theme.spacing(1.5),
    alignItems: 'center',
    justifyContent: 'center',
    ...theme.shadow.base,
  },
  buttonText: {
    color: 'white',
    fontWeight: '700',
  },
  chip: {
    backgroundColor: '#eef7f0',
    borderRadius: theme.radius.sm,
    paddingHorizontal: theme.spacing(1),
    paddingVertical: theme.spacing(0.5),
    marginRight: theme.spacing(1),
    marginBottom: theme.spacing(0.5),
  },
  chipText: {
    color: theme.colors.primaryDark,
    fontWeight: '600',
  },
});

export { theme };
