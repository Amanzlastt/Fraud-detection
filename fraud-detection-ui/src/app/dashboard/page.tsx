"use client";

import { useState, useEffect } from "react";
import { 
  TrendingUp, 
  TrendingDown, 
  AlertTriangle, 
  CheckCircle,
  Activity,
  DollarSign,
  Users,
  Shield,
  Search,
  BarChart3,
  Settings
} from "lucide-react";

interface DashboardStats {
  totalTransactions: number;
  fraudCases: number;
  fraudPercentage: number;
  recentFraudTrend: number;
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats>({
    totalTransactions: 0,
    fraudCases: 0,
    fraudPercentage: 0,
    recentFraudTrend: 0,
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // In a real app, you'd fetch this from your API
    // For now, using mock data
    setTimeout(() => {
      setStats({
        totalTransactions: 15420,
        fraudCases: 1234,
        fraudPercentage: 8.0,
        recentFraudTrend: -2.5,
      });
      setIsLoading(false);
    }, 1000);
  }, []);

  const cards = [
    {
      name: "Total Transactions",
      value: stats.totalTransactions.toLocaleString(),
      icon: Activity,
      change: "+12.5%",
      changeType: "positive" as const,
    },
    {
      name: "Fraud Cases",
      value: stats.fraudCases.toLocaleString(),
      icon: AlertTriangle,
      change: `${stats.recentFraudTrend > 0 ? '+' : ''}${stats.recentFraudTrend}%`,
      changeType: stats.recentFraudTrend < 0 ? "positive" : "negative" as const,
    },
    {
      name: "Fraud Rate",
      value: `${stats.fraudPercentage}%`,
      icon: Shield,
      change: "-0.5%",
      changeType: "positive" as const,
    },
    {
      name: "Success Rate",
      value: `${100 - stats.fraudPercentage}%`,
      icon: CheckCircle,
      change: "+0.5%",
      changeType: "positive" as const,
    },
  ];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Overview of fraud detection system performance</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map((card) => (
          <div
            key={card.name}
            className="bg-white overflow-hidden shadow rounded-lg"
          >
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <card.icon className="h-6 w-6 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      {card.name}
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {card.value}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
            <div className="bg-gray-50 px-5 py-3">
              <div className="text-sm">
                <span
                  className={`font-medium ${
                    card.changeType === "positive"
                      ? "text-green-600"
                      : "text-red-600"
                  }`}
                >
                  {card.changeType === "positive" ? (
                    <TrendingUp className="inline h-4 w-4" />
                  ) : (
                    <TrendingDown className="inline h-4 w-4" />
                  )}
                  {card.change}
                </span>
                <span className="text-gray-500"> from last month</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Recent Activity
          </h3>
          <div className="mt-5">
            <div className="space-y-4">
              {[
                {
                  type: "fraud",
                  message: "Suspicious transaction detected",
                  time: "2 minutes ago",
                  amount: "$1,250.00",
                },
                {
                  type: "legitimate",
                  message: "Transaction approved",
                  time: "5 minutes ago",
                  amount: "$89.99",
                },
                {
                  type: "fraud",
                  message: "High-risk transaction flagged",
                  time: "12 minutes ago",
                  amount: "$2,500.00",
                },
                {
                  type: "legitimate",
                  message: "Transaction approved",
                  time: "15 minutes ago",
                  amount: "$45.50",
                },
              ].map((activity, index) => (
                <div key={index} className="flex items-center space-x-3">
                  <div
                    className={`flex-shrink-0 h-2 w-2 rounded-full ${
                      activity.type === "fraud"
                        ? "bg-red-400"
                        : "bg-green-400"
                    }`}
                  />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">
                      {activity.message}
                    </p>
                    <p className="text-sm text-gray-500">{activity.time}</p>
                  </div>
                  <div className="flex-shrink-0 text-sm font-medium text-gray-900">
                    {activity.amount}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Quick Actions
          </h3>
          <div className="mt-5 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <button className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg border border-gray-200 hover:border-gray-300">
              <div>
                <span className="rounded-lg inline-flex p-3 bg-blue-50 text-blue-700 ring-4 ring-white">
                  <Search className="h-6 w-6" />
                </span>
              </div>
              <div className="mt-8">
                <h3 className="text-lg font-medium">
                  <span className="absolute inset-0" aria-hidden="true" />
                  New Detection
                </h3>
                <p className="mt-2 text-sm text-gray-500">
                  Run fraud detection on a new transaction
                </p>
              </div>
            </button>

            <button className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg border border-gray-200 hover:border-gray-300">
              <div>
                <span className="rounded-lg inline-flex p-3 bg-green-50 text-green-700 ring-4 ring-white">
                  <BarChart3 className="h-6 w-6" />
                </span>
              </div>
              <div className="mt-8">
                <h3 className="text-lg font-medium">
                  <span className="absolute inset-0" aria-hidden="true" />
                  View Reports
                </h3>
                <p className="mt-2 text-sm text-gray-500">
                  Access detailed analytics and reports
                </p>
              </div>
            </button>

            <button className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg border border-gray-200 hover:border-gray-300">
              <div>
                <span className="rounded-lg inline-flex p-3 bg-purple-50 text-purple-700 ring-4 ring-white">
                  <Settings className="h-6 w-6" />
                </span>
              </div>
              <div className="mt-8">
                <h3 className="text-lg font-medium">
                  <span className="absolute inset-0" aria-hidden="true" />
                  Settings
                </h3>
                <p className="mt-2 text-sm text-gray-500">
                  Configure system parameters
                </p>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
} 