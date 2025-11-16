'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { supabase } from '@/lib/supabase'

interface UserProfile {
  user_id: string
  display_name: string | null
  reputation_points: number
  parts_added: number
  parts_verified: number
  accuracy_score: number
  badges: any[]
}

export default function LeaderboardPage() {
  const [users, setUsers] = useState<UserProfile[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadLeaderboard()
  }, [])

  const loadLeaderboard = async () => {
    setLoading(true)
    try {
      const { data, error } = await supabase
        .from('user_profiles')
        .select('*')
        .order('reputation_points', { ascending: false })
        .limit(100)

      if (error) throw error
      setUsers(data || [])
    } catch (err) {
      console.error('Failed to load leaderboard:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-slate-900">
                Leaderboard
              </h1>
              <p className="mt-1 text-sm text-slate-600">
                Top contributors to the Universal Parts Database
              </p>
            </div>
            <Link
              href="/"
              className="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition-colors font-medium"
            >
              Back
            </Link>
          </div>
        </div>
      </header>

      {/* Leaderboard */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        ) : users.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-12 text-center">
            <p className="text-slate-600">No users yet. Be the first to contribute!</p>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
            <table className="min-w-full divide-y divide-slate-200">
              <thead className="bg-slate-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Rank
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    User
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Reputation
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Parts Added
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Verified
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Accuracy
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Badges
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-slate-200">
                {users.map((user, idx) => (
                  <tr key={user.user_id} className={idx < 3 ? 'bg-yellow-50' : ''}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {idx === 0 && <span className="text-2xl mr-2">🥇</span>}
                        {idx === 1 && <span className="text-2xl mr-2">🥈</span>}
                        {idx === 2 && <span className="text-2xl mr-2">🥉</span>}
                        <span className="text-sm font-medium text-slate-900">#{idx + 1}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-slate-900">
                        {user.display_name || `User ${user.user_id.slice(0, 8)}`}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-bold text-blue-600">
                        {user.reputation_points}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-slate-600">
                        {user.parts_added}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-slate-600">
                        {user.parts_verified}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-slate-600">
                        {user.accuracy_score.toFixed(1)}%
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex space-x-1">
                        {user.badges && user.badges.length > 0 ? (
                          user.badges.slice(0, 3).map((badge: any, i: number) => (
                            <span
                              key={i}
                              className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-purple-100 text-purple-800"
                              title={badge.name}
                            >
                              {badge.icon || '🏆'}
                            </span>
                          ))
                        ) : (
                          <span className="text-xs text-slate-400">None yet</span>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Badges Info */}
        <div className="mt-8 bg-white rounded-lg shadow-sm border border-slate-200 p-6">
          <h2 className="text-xl font-semibold text-slate-900 mb-4">Available Badges</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div className="border border-slate-200 rounded-lg p-4">
              <div className="flex items-center">
                <span className="text-2xl mr-3">🎯</span>
                <div>
                  <h3 className="font-medium text-slate-900">First Contribution</h3>
                  <p className="text-sm text-slate-600">Add your first part</p>
                </div>
              </div>
            </div>
            <div className="border border-slate-200 rounded-lg p-4">
              <div className="flex items-center">
                <span className="text-2xl mr-3">📏</span>
                <div>
                  <h3 className="font-medium text-slate-900">Metric Master</h3>
                  <p className="text-sm text-slate-600">50+ metric parts</p>
                </div>
              </div>
            </div>
            <div className="border border-slate-200 rounded-lg p-4">
              <div className="flex items-center">
                <span className="text-2xl mr-3">🇺🇸</span>
                <div>
                  <h3 className="font-medium text-slate-900">Imperial Expert</h3>
                  <p className="text-sm text-slate-600">50+ imperial parts</p>
                </div>
              </div>
            </div>
            <div className="border border-slate-200 rounded-lg p-4">
              <div className="flex items-center">
                <span className="text-2xl mr-3">✅</span>
                <div>
                  <h3 className="font-medium text-slate-900">Verifier</h3>
                  <p className="text-sm text-slate-600">Verify 100 parts</p>
                </div>
              </div>
            </div>
            <div className="border border-slate-200 rounded-lg p-4">
              <div className="flex items-center">
                <span className="text-2xl mr-3">🌟</span>
                <div>
                  <h3 className="font-medium text-slate-900">Trusted Source</h3>
                  <p className="text-sm text-slate-600">95%+ accuracy</p>
                </div>
              </div>
            </div>
            <div className="border border-slate-200 rounded-lg p-4">
              <div className="flex items-center">
                <span className="text-2xl mr-3">👑</span>
                <div>
                  <h3 className="font-medium text-slate-900">Community Leader</h3>
                  <p className="text-sm text-slate-600">1000+ reputation</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
