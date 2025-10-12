import React, { useState } from 'react';
import { SafeAreaView, View, Pressable, Text } from 'react-native';
import OnboardingScreen from './screens/OnboardingScreen';
import RadarScreen from './screens/RadarScreen';
import RecipesScreen from './screens/RecipesScreen';
import FeedbackScreen from './screens/FeedbackScreen';
import { useTasteProfile } from './hooks/useTasteProfile';
import { styles, theme } from './styles/styles';

export default function App() {
  const [screen, setScreen] = useState('onboarding'); // 'onboarding' | 'radar' | 'recipes' | 'feedback'
  const { vUser, initProfile, updateProfile, selectedRecipe, selectRecipe } = useTasteProfile();

  return (
    <SafeAreaView style={styles.screen}>
      {screen === 'onboarding' && (
        <OnboardingScreen
          onComplete={(v) => {
            initProfile(v);
            setScreen('radar');
          }}
        />
      )}
      {screen === 'radar' && <RadarScreen vUser={vUser} onGoRecipes={() => setScreen('recipes')} />}
      {screen === 'recipes' && (
        <RecipesScreen
          vUser={vUser}
          onSelectRecipe={(r) => {
            selectRecipe(r);
            setScreen('feedback');
          }}
        />
      )}
      {screen === 'feedback' && selectedRecipe && (
        <FeedbackScreen
          vUser={vUser}
          recipe={selectedRecipe}
          onRated={(r) => {
            updateProfile(selectedRecipe.v, r);
            setScreen('radar');
          }}
        />
      )}

      {/* Simple footer nav */}
      <View style={{ flexDirection: 'row', justifyContent: 'space-around', padding: 10, borderTopWidth: 1, borderColor: theme.colors.border }}>
        {['onboarding', 'radar', 'recipes'].map((key) => (
          <Pressable key={key} onPress={() => setScreen(key)}>
            <Text style={{ fontWeight: screen === key ? '800' : '600', color: theme.colors.primary }}>
              {key === 'onboarding' ? 'Quiz' : key.charAt(0).toUpperCase() + key.slice(1)}
            </Text>
          </Pressable>
        ))}
      </View>
    </SafeAreaView>
  );
}
