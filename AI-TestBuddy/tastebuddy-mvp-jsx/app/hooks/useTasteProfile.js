import { useEffect, useState } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { ewmaUpdate } from '../utils/math';

export function useTasteProfile() {
  const [vUser, setVUser] = useState(Array(7).fill(0.5));
  const [selectedRecipe, setSelectedRecipe] = useState(null);

  useEffect(() => {
    AsyncStorage.getItem('tasteProfile').then((data) => {
      if (data) setVUser(JSON.parse(data));
    });
  }, []);

  const initProfile = async (v0) => {
    setVUser(v0);
    await AsyncStorage.setItem('tasteProfile', JSON.stringify(v0));
  };

  const updateProfile = async (vRecipe, rating) => {
    const vNew = ewmaUpdate(vUser, vRecipe, rating);
    setVUser(vNew);
    await AsyncStorage.setItem('tasteProfile', JSON.stringify(vNew));
  };

  const selectRecipe = (r) => setSelectedRecipe(r);

  return { vUser, initProfile, updateProfile, selectedRecipe, selectRecipe };
}
