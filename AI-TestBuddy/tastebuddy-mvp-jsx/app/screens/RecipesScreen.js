import React, { useMemo, useState } from 'react';
import { SafeAreaView, Text, TextInput, FlatList } from 'react-native';
import { getRecipes } from '../data/recipes';
import { cosine } from '../utils/math';
import { RecipeCard } from '../components/RecipeCard';
import { styles } from '../styles/styles';

export default function RecipesScreen({ vUser, onSelectRecipe }) {
  const [have, setHave] = useState('');
  const recipes = getRecipes();

  const ranked = useMemo(() => {
    const haveSet = new Set(have.split(',').map((x) => x.trim().toLowerCase()).filter(Boolean));
    return recipes
      .map((r) => {
        const base = cosine(vUser, r.v);
        const inv = haveSet.size ? r.ingredients.filter((x) => haveSet.has(x.toLowerCase())).length / haveSet.size : 0;
        const score = 0.75 * base + 0.25 * inv;
        return { ...r, score };
      })
      .sort((a, b) => b.score - a.score);
  }, [vUser, have]);

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: 'white', padding: 16 }}>
      <Text style={styles.title}>Recomendaciones</Text>
      <TextInput
        placeholder="Ingredientes que tienes (coma separada)"
        value={have}
        onChangeText={setHave}
        style={{ borderWidth: 1, borderColor: '#ddd', padding: 10, borderRadius: 10, marginBottom: 12 }}
      />

      <FlatList
        data={ranked}
        keyExtractor={(r) => r.id.toString()}
        renderItem={({ item }) => <RecipeCard item={item} onSelect={() => onSelectRecipe(item)} />}
      />
    </SafeAreaView>
  );
}
