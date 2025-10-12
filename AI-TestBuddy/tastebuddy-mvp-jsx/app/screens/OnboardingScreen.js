import React, { useState } from 'react';
import { View, Text, ScrollView } from 'react-native';
import { Button } from '../components/Button';
import { RadarChart } from '../components/RadarChart';
import { styles } from '../styles/styles';

const DIMENSIONS = [
  { key: 'dulce', label: 'Dulce' },
  { key: 'salado', label: 'Salado' },
  { key: 'acido', label: 'Ácido' },
  { key: 'amargo', label: 'Amargo' },
  { key: 'umami', label: 'Umami' },
  { key: 'picante', label: 'Picante' },
  { key: 'crujiente', label: 'Crujiente' },
];

export default function OnboardingScreen({ onComplete }) {
  const [vals, setVals] = useState(DIMENSIONS.map(() => 0.5));
  const setVal = (i, v) => {
    const nv = [...vals];
    nv[i] = Math.max(0, Math.min(1, v));
    setVals(nv);
  };

  return (
    <ScrollView contentContainerStyle={{ padding: 20, backgroundColor: 'white' }}>
      <Text style={styles.title}>Tu perfil de sabor</Text>
      <Text style={styles.subtitle}>Ajusta cuánto te gusta cada dimensión.</Text>

      {DIMENSIONS.map((d, i) => (
        <View key={d.key} style={styles.card}>
          <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
            <Text style={{ fontWeight: '700' }}>{d.label}</Text>
            <Text>{(vals[i] * 100).toFixed(0)}%</Text>
          </View>
          <View style={{ flexDirection: 'row', marginTop: 10, alignItems: 'center' }}>
            <Button title="-" onPress={() => setVal(i, vals[i] - 0.1)} style={{ width: 48 }} />
            <View style={{ flex: 1, height: 8, marginHorizontal: 8, backgroundColor: '#f0f0f0', borderRadius: 10 }}>
              <View style={{ width: `${vals[i] * 100}%`, height: 8, backgroundColor: '#28a745', borderRadius: 10 }} />
            </View>
            <Button title="+" onPress={() => setVal(i, vals[i] + 0.1)} style={{ width: 48 }} />
          </View>
        </View>
      ))}

      <View style={{ alignItems: 'center', marginVertical: 20 }}>
        <RadarChart values={vals} />
      </View>

      <Button title="Continuar" onPress={() => onComplete(vals)} />
    </ScrollView>
  );
}
