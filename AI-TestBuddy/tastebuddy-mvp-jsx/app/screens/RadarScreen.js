import React from 'react';
import { View, Text } from 'react-native';
import { Button } from '../components/Button';
import { RadarChart } from '../components/RadarChart';
import { styles } from '../styles/styles';

export default function RadarScreen({ vUser, onGoRecipes }) {
  return (
    <View style={{ flex: 1, backgroundColor: 'white', padding: 16 }}>
      <Text style={styles.title}>Mapa de sabor</Text>
      <Text style={styles.subtitle}>Este es tu perfil actual.</Text>
      <View style={{ alignItems: 'center', marginVertical: 16 }}>
        <RadarChart values={vUser} />
      </View>
      <Button title="Ver recomendaciones" onPress={onGoRecipes} />
    </View>
  );
}
