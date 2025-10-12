import React from 'react';
import { Pressable, Text, View } from 'react-native';
import { Chip } from './Chip';

export const RecipeCard = ({ item, onSelect }) => (
  <Pressable onPress={() => onSelect(item)} style={{ borderWidth: 1, borderColor: '#eee', borderRadius: 12, padding: 14, marginBottom: 12 }}>
    <Text style={{ fontSize: 16, fontWeight: '800' }}>{item.title}</Text>
    <Text style={{ color: '#666', marginVertical: 6 }}>Compatibilidad: {(item.score * 100).toFixed(0)}%</Text>
    <View style={{ flexDirection: 'row', flexWrap: 'wrap' }}>
      {item.tags.map((t) => <Chip key={t} label={t} />)}
    </View>
    <Text style={{ marginTop: 8, color: '#333' }}>Ingredientes: {item.ingredients.join(', ')}</Text>
  </Pressable>
);
